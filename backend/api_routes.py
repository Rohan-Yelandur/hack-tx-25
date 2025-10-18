from flask import request, jsonify, send_file
from pathlib import Path
from gemini_service import gemini_service
from elevenlabs_service import eleven_labs_service
from manim_service import manim_service
import threading


def register_routes(app):
    """Register all API routes with the Flask app."""
    
    @app.route('/api/generate-video', methods=['POST'])
    def generate_video():
        """Generate a Manim video with synchronized narration.
        
        New flow:
        1. Generate narration script from user prompt
        2. Generate audio with character-level timing data
        3. Use script + timing to generate synchronized Manim code
        4. Render video
        """
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        try:
            print(f"\n{'='*60}")
            print(f"[API] Starting video generation for prompt: {prompt[:50]}...")
            print(f"{'='*60}\n")
            
            # Step 1: Generate narration script first
            print("[API] Step 1: Generating narration script...")
            narration_script = eleven_labs_service.generate_script(prompt)
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
                response['video_url'] = f'/api/manim-video/{Path(video_result["path"]).name}'
                response['manim_code_url'] = f'/api/manim-code/{Path(video_result["manim_code_path"]).name}'
                response['manim_code'] = video_result['manim_code']
            else:
                response['video_error'] = video_result['error'] or 'Failed to render video'
                # Don't mark as completely failed if audio succeeded
                if not audio_result['path']:
                    response['success'] = False
            
            # Return error if both failed
            if not video_result['path'] and not audio_result['path']:
                return jsonify(response), 500
            
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
            
            return jsonify({
                'success': True,
                'script_url': f'/api/elevenlabs-script/{script_filename}',
                'audio_url': f'/api/elevenlabs-audio/{audio_filename}',
                'script_text': narration_script,
                'audio_duration': timing_data['character_end_times'][-1] if timing_data['character_end_times'] else 0
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