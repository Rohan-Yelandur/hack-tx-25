from flask import request, jsonify, send_file
from pathlib import Path
from gemini_service import gemini_service
from elevenlabs_service import eleven_labs_service
from manim_service import manim_service
import threading
import os
import re
from werkzeug.utils import secure_filename
import json


def register_routes(app):
    """Register all API routes with the Flask app."""

    COMMUNITY_FILE = Path('community_videos.json')

    def load_community_videos():
        """Load the list of community video IDs from JSON file."""
        if not COMMUNITY_FILE.exists():
            return []
        try:
            with open(COMMUNITY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_community_videos(video_ids):
        """Save the list of community video IDs to JSON file."""
        try:
            with open(COMMUNITY_FILE, 'w') as f:
                json.dump(video_ids, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving community videos: {e}")
            return False

    @app.route('/api/generate-video', methods=['POST'])
    def generate_video():
        """Generate a Manim video with synchronized narration.
        
        New flow:
        1. Generate narration script from user prompt (with optional PDF)
        2. Generate audio with character-level timing data
        3. Use script + timing to generate synchronized Manim code
        4. Render video
        """
        # Handle both JSON and FormData
        if request.content_type and 'multipart/form-data' in request.content_type:
            prompt = request.form.get('prompt', '')
            pdf_file = request.files.get('pdf', None)
        else:
            data = request.json or {}
            prompt = data.get('prompt', '')
            pdf_file = None
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Handle PDF file if provided
        pdf_path = None
        if pdf_file and pdf_file.filename:
            try:
                from settings import settings
                # Create temporary upload directory if needed
                upload_dir = Path(settings.CODE_DIR).parent / 'temp_uploads'
                upload_dir.mkdir(exist_ok=True)
                
                # Save PDF with secure filename
                filename = secure_filename(pdf_file.filename)
                pdf_path = upload_dir / filename
                pdf_file.save(str(pdf_path))
                print(f"[API] PDF uploaded: {pdf_path}")
            except Exception as e:
                print(f"[API] Error saving PDF: {str(e)}")
                pdf_path = None
        
        try:
            print(f"\n{'='*60}")
            print(f"[API] Starting video generation for prompt: {prompt[:50]}...")
            if pdf_path:
                print(f"[API] With PDF file: {pdf_path.name}")
            print(f"{'='*60}\n")
            
            # Step 1: Generate narration script first (with PDF if provided)
            print("[API] Step 1: Generating narration script...")
            narration_script = eleven_labs_service.generate_script(prompt, pdf_path=pdf_path)
            print(f"[API] Script generated: {narration_script[:100]}...\n")
            
            # Prepare storage for parallel results
            audio_result = {'path': None, 'script_path': None, 'timing_data': None, 'error': None}
            video_result = {'path': None, 'manim_code_path': None, 'manim_code': None, 'error': None}
            
            # Create an event to signal when audio (and timing data) is ready
            audio_ready = threading.Event()
            
            # Thread 1: Generate audio with timing data
            def generate_audio():
                try:
                    print("[API-AudioThread] Starting audio generation...")
                    audio_path, script_path, timing_data = eleven_labs_service.generate_audio_with_timestamps(narration_script)
                    audio_result['path'] = audio_path
                    audio_result['script_path'] = script_path
                    audio_result['timing_data'] = timing_data
                    print(f"[API-AudioThread] Audio generation complete: {audio_path}")
                    # Signal that audio and timing data are ready
                    audio_ready.set()
                except Exception as e:
                    error_msg = f"{type(e).__name__}: {str(e)}"
                    print(f"[API-AudioThread ERROR] {error_msg}")
                    import traceback
                    traceback.print_exc()
                    audio_result['error'] = error_msg
                    audio_ready.set()  # Signal even on error so video thread doesn't hang
            
            # Thread 2: Generate Manim code and render video (waits for timing data)
            def generate_and_render_video():
                try:
                    print("[API-VideoThread] Waiting for audio/timing data...")
                    # Wait for audio thread to complete and provide timing data
                    audio_ready.wait()
                    
                    # Check if audio generation succeeded
                    if audio_result['error']:
                        video_result['error'] = f"Cannot generate video: audio generation failed - {audio_result['error']}"
                        print(f"[API-VideoThread ERROR] {video_result['error']}")
                        return
                    
                    print("[API-VideoThread] Audio ready, generating Manim code...")
                    # Generate Manim code using script and timing data
                    manim_code = gemini_service.generate_manim_code_from_script(
                        prompt, 
                        narration_script, 
                        audio_result['timing_data']
                    )
                    video_result['manim_code'] = manim_code
                    
                    print("[API-VideoThread] Rendering video...")
                    # Render the video
                    video_path, manim_code_path = manim_service.render_manim_video(manim_code)
                    video_result['path'] = video_path
                    video_result['manim_code_path'] = manim_code_path
                    print(f"[API-VideoThread] Video rendering complete: {video_path}")
                except Exception as e:
                    error_msg = f"{type(e).__name__}: {str(e)}"
                    print(f"[API-VideoThread ERROR] {error_msg}")
                    import traceback
                    traceback.print_exc()
                    video_result['error'] = error_msg
            
            # Start both threads in parallel (after script generation)
            print("[API] Step 2: Starting parallel audio and video generation threads...")
            audio_thread = threading.Thread(target=generate_audio)
            video_thread = threading.Thread(target=generate_and_render_video)
            
            audio_thread.start()
            video_thread.start()
            
            # Wait for both to complete
            audio_thread.join()
            video_thread.join()
            print("[API] Both threads completed\n")
            
            # Build response
            response = {
                'success': True,
                'script_text': narration_script
            }
            
            # Add audio results
            if audio_result['path']:
                response['audio_url'] = f'/api/elevenlabs-audio/{Path(audio_result["path"]).name}'
                response['script_url'] = f'/api/elevenlabs-script/{Path(audio_result["script_path"]).name}'
            else:
                response['audio_error'] = audio_result['error'] or 'Failed to generate audio'
                response['success'] = False
            
            # Add video results
            if video_result['path']:
                video_filename = Path(video_result["path"]).name
                # Extract video ID from filename (e.g., "20251018_195826.mp4" -> "20251018_195826")
                video_id = re.match(r'(\d{8}_\d{6})\.mp4', video_filename)
                response['video_url'] = f'/api/manim-video/{video_filename}'
                response['manim_code_url'] = f'/api/manim-code/{Path(video_result["manim_code_path"]).name}'
                response['manim_code'] = video_result['manim_code']
                if video_id:
                    response['video_id'] = video_id.group(1)
            else:
                response['video_error'] = video_result['error'] or 'Failed to render video'
                # Don't mark as completely failed if audio succeeded
                if not audio_result['path']:
                    response['success'] = False
            
            # Return error if both failed
            if not video_result['path'] and not audio_result['path']:
                return jsonify(response), 500
            
            # Clean up temporary PDF file if it exists
            if pdf_path and pdf_path.exists():
                try:
                    pdf_path.unlink()
                    print(f"[API] Cleaned up temporary PDF: {pdf_path}")
                except Exception as e:
                    print(f"[API] Failed to clean up PDF: {str(e)}")
            
            return jsonify(response)
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"\n[API ERROR] Video generation failed: {error_msg}")
            import traceback
            traceback.print_exc()
            print(f"{'='*60}\n")
            return jsonify({
                'error': error_msg,
                'error_type': type(e).__name__
            }), 500
    
    
    @app.route('/api/generate-narration', methods=['POST'])
    def generate_narration():
        """Generate narration script and audio for a given prompt."""
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        try:
            print(f"\n[API-Narration] Generating narration for prompt: {prompt[:50]}...")
            
            # Generate script from prompt
            narration_script = eleven_labs_service.generate_script(prompt)
            
            # Generate audio with timestamps
            audio_path, script_path, timing_data = eleven_labs_service.generate_audio_with_timestamps(narration_script)
            
            audio_filename = Path(audio_path).name
            script_filename = Path(script_path).name
            
            print(f"[API-Narration] Narration generation complete\n")
            
            # Extract duration from timing data
            char_timings = timing_data.get('character_timings', {})
            audio_duration = char_timings.get('character_end_times', [0])[-1] if char_timings.get('character_end_times') else 0
            
            return jsonify({
                'success': True,
                'script_url': f'/api/elevenlabs-script/{script_filename}',
                'audio_url': f'/api/elevenlabs-audio/{audio_filename}',
                'script_text': narration_script,
                'audio_duration': audio_duration
            })
                
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[API-Narration ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': error_msg,
                'error_type': type(e).__name__
            }), 500
    


    @app.route('/api/videos', methods=['GET'])
    def get_all_videos():
        """Get a list of community videos with their associated files.

        This endpoint scans the filesystem for videos marked as community
        and matches them with their corresponding audio, script, and code files.

        Note: This is a file-based implementation. Can be easily replaced with
        a database query in the future without changing the API response format.
        """
        try:
            from settings import settings

            print("[API-Videos] Fetching community videos...")

            # Load community video IDs
            community_video_ids = load_community_videos()
            print(f"[API-Videos] Found {len(community_video_ids)} community videos")

            # Get all video files
            video_dir = Path(settings.OUTPUT_DIR)
            if not video_dir.exists():
                return jsonify({'success': True, 'videos': []})

            video_files = sorted(video_dir.glob('*.mp4'), key=os.path.getmtime, reverse=True)

            # Get all audio and script files upfront
            audio_dir = Path(settings.AUDIO_DIR)
            script_dir = Path(settings.SCRIPTS_DIR)
            code_dir = Path(settings.CODE_DIR)

            all_audio_files = {af: af.stat().st_mtime for af in audio_dir.glob('audio_*.mp3')}
            all_script_files = {sf: sf.stat().st_mtime for sf in script_dir.glob('script_*.txt')}

            # Track which files have been matched to avoid duplicates
            matched_audio = set()
            matched_scripts = set()

            videos = []
            for video_path in video_files:
                # Extract timestamp from filename (e.g., "20251018_195826.mp4")
                video_filename = video_path.name
                timestamp_match = re.match(r'(\d{8}_\d{6})\.mp4', video_filename)

                if not timestamp_match:
                    continue

                timestamp = timestamp_match.group(1)

                # Only include videos marked as community
                if timestamp not in community_video_ids:
                    continue
                video_mtime = video_path.stat().st_mtime

                # Try to find matching audio file
                # First try exact timestamp match
                exact_audio = audio_dir / f'audio_{timestamp}.mp3'
                audio_path = None

                if exact_audio.exists() and exact_audio not in matched_audio:
                    audio_path = exact_audio
                    matched_audio.add(exact_audio)
                else:
                    # Find closest unmatched audio file by modification time
                    unmatched_audio = {af: mtime for af, mtime in all_audio_files.items()
                                      if af not in matched_audio}
                    if unmatched_audio:
                        closest_audio = min(
                            unmatched_audio.keys(),
                            key=lambda af: abs(unmatched_audio[af] - video_mtime)
                        )
                        # Only use if within 2 minutes (120 seconds)
                        if abs(unmatched_audio[closest_audio] - video_mtime) < 120:
                            audio_path = closest_audio
                            matched_audio.add(closest_audio)

                # Try to find matching script file
                # First try exact timestamp match
                exact_script = script_dir / f'script_{timestamp}.txt'
                script_path = None
                script_text = None

                if exact_script.exists() and exact_script not in matched_scripts:
                    script_path = exact_script
                    matched_scripts.add(exact_script)
                else:
                    # Find closest unmatched script file by modification time
                    unmatched_scripts = {sf: mtime for sf, mtime in all_script_files.items()
                                        if sf not in matched_scripts}
                    if unmatched_scripts:
                        closest_script = min(
                            unmatched_scripts.keys(),
                            key=lambda sf: abs(unmatched_scripts[sf] - video_mtime)
                        )
                        # Only use if within 2 minutes (120 seconds)
                        if abs(unmatched_scripts[closest_script] - video_mtime) < 120:
                            script_path = closest_script
                            matched_scripts.add(closest_script)

                # Read script text if found
                if script_path:
                    try:
                        script_text = script_path.read_text(encoding='utf-8')
                    except:
                        script_text = None

                # Try to find matching code file
                code_files = list(code_dir.glob(f'{timestamp}.py'))
                code_path = code_files[0] if code_files else None

                # Build video entry
                video_entry = {
                    'id': timestamp,
                    'video_url': f'/api/manim-video/{video_filename}',
                    'created_at': os.path.getmtime(video_path)
                }

                if audio_path:
                    video_entry['audio_url'] = f'/api/elevenlabs-audio/{audio_path.name}'

                if script_path:
                    video_entry['script_url'] = f'/api/elevenlabs-script/{script_path.name}'
                    if script_text:
                        video_entry['script_text'] = script_text

                if code_path:
                    video_entry['manim_code_url'] = f'/api/manim-code/{code_path.name}'

                videos.append(video_entry)

            print(f"[API-Videos] Found {len(videos)} videos")

            return jsonify({
                'success': True,
                'videos': videos
            })

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[API-Videos ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': error_msg,
                'error_type': type(e).__name__
            }), 500


    @app.route('/api/videos/<video_id>/share-to-community', methods=['POST'])
    def share_to_community(video_id):
        """Mark a video as shared to the community."""
        try:
            from settings import settings

            # Verify the video exists
            video_dir = Path(settings.OUTPUT_DIR)
            video_path = video_dir / f'{video_id}.mp4'

            if not video_path.exists():
                return jsonify({
                    'error': 'Video not found',
                    'success': False
                }), 404

            # Load current community videos
            community_videos = load_community_videos()

            # Check if already shared
            if video_id in community_videos:
                return jsonify({
                    'success': True,
                    'message': 'Video already shared to community',
                    'video_id': video_id
                })

            # Add to community
            community_videos.append(video_id)

            if save_community_videos(community_videos):
                print(f"[API-Community] Video {video_id} shared to community")
                return jsonify({
                    'success': True,
                    'message': 'Video shared to community',
                    'video_id': video_id
                })
            else:
                return jsonify({
                    'error': 'Failed to save community data',
                    'success': False
                }), 500

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[API-Community ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': error_msg,
                'error_type': type(e).__name__,
                'success': False
            }), 500


    @app.route('/api/videos/<video_id>/remove-from-community', methods=['POST'])
    def remove_from_community(video_id):
        """Remove a video from the community."""
        try:
            # Load current community videos
            community_videos = load_community_videos()

            # Check if video is in community
            if video_id not in community_videos:
                return jsonify({
                    'success': True,
                    'message': 'Video not in community'
                })

            # Remove from community
            community_videos.remove(video_id)

            if save_community_videos(community_videos):
                print(f"[API-Community] Video {video_id} removed from community")
                return jsonify({
                    'success': True,
                    'message': 'Video removed from community',
                    'video_id': video_id
                })
            else:
                return jsonify({
                    'error': 'Failed to save community data',
                    'success': False
                }), 500

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[API-Community ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': error_msg,
                'error_type': type(e).__name__,
                'success': False
            }), 500


    # ==================== Resource Endpoints ====================

    @app.route('/api/manim-video/<filename>', methods=['GET'])
    def get_manim_video(filename):
        """Serve Manim video files."""
        video_path = manim_service.get_video_path(filename)
        if video_path.exists():
            return send_file(video_path, mimetype='video/mp4')
        return jsonify({'error': 'Video not found'}), 404
    
    
    @app.route('/api/manim-code/<filename>', methods=['GET'])
    def get_manim_code(filename):
        """Serve Manim code/script files."""
        script_path = manim_service.get_script_path(filename)
        if script_path.exists():
            return send_file(script_path, mimetype='text/plain')
        return jsonify({'error': 'Script not found'}), 404
    
    
    @app.route('/api/elevenlabs-script/<filename>', methods=['GET'])
    def get_elevenlabs_script(filename):
        """Serve ElevenLabs narration script files."""
        from settings import settings
        script_path = Path(settings.SCRIPTS_DIR) / filename
        if script_path.exists():
            return send_file(script_path, mimetype='text/plain')
        return jsonify({'error': 'Narration script not found'}), 404
    
    
    @app.route('/api/elevenlabs-audio/<filename>', methods=['GET'])
    def get_elevenlabs_audio(filename):
        """Serve ElevenLabs audio files."""
        from settings import settings
        audio_path = Path(settings.AUDIO_DIR) / filename
        if audio_path.exists():
            return send_file(audio_path, mimetype='audio/mpeg')
        return jsonify({'error': 'Audio not found'}), 404