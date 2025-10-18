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
        """Generate a Manim video with synchronized narration using parallel processing."""
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        try:
            # Step 1: Generate Manim code with detailed comments for narration
            manim_code = gemini_service.generate_manim_code(prompt)
            
            # Prepare storage for parallel results
            video_result = {'path': None, 'script_path': None, 'error': None}
            audio_result = {'audio_path': None, 'script_path': None, 'script_text': None, 'error': None}
            
            # Thread 1: Render Manim video
            def render_video():
                try:
                    video_path, script_path = manim_service.render_manim_video(manim_code)
                    video_result['path'] = video_path
                    video_result['script_path'] = script_path
                except Exception as e:
                    video_result['error'] = str(e)
            
            # Thread 2: Generate narration from Manim code comments, then create audio
            def generate_narration():
                try:
                    # Use Manim code comments to generate synchronized narration
                    audio_path, script_path, script_text = eleven_labs_service.generate_audio_from_prompt(prompt, manim_code)
                    audio_result['audio_path'] = audio_path
                    audio_result['script_path'] = script_path
                    audio_result['script_text'] = script_text
                except Exception as e:
                    audio_result['error'] = str(e)
            
            # Start both threads in parallel
            video_thread = threading.Thread(target=render_video)
            audio_thread = threading.Thread(target=generate_narration)
            
            video_thread.start()
            audio_thread.start()
            
            # Wait for both to complete
            video_thread.join()
            audio_thread.join()
            
            # Build response
            response = {
                'success': True,
                'manim_code': manim_code
            }
            
            # Add video results
            if video_result['path']:
                response['video_url'] = f'/api/manim-video/{Path(video_result["path"]).name}'
                response['manim_code_url'] = f'/api/manim-code/{Path(video_result["script_path"]).name}'
            else:
                response['video_error'] = video_result['error'] or 'Failed to render video'
                response['success'] = False
            
            # Add audio results
            if audio_result['audio_path']:
                response['audio_url'] = f'/api/elevenlabs-audio/{Path(audio_result["audio_path"]).name}'
                response['script_url'] = f'/api/elevenlabs-script/{Path(audio_result["script_path"]).name}'
                response['script_text'] = audio_result['script_text']
            else:
                response['audio_error'] = audio_result['error'] or 'Failed to generate audio'
            
            # Return error if both failed
            if not video_result['path'] and not audio_result['audio_path']:
                return jsonify(response), 500
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/generate-narration', methods=['POST'])
    def generate_narration():
        """Generate narration script and audio for a given prompt."""
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        try:
            # For standalone narration, generate without manim code context
            audio_path, script_path, narration_script = eleven_labs_service.generate_audio_from_prompt(prompt, "")
            
            audio_filename = Path(audio_path).name
            script_filename = Path(script_path).name
            
            return jsonify({
                'success': True,
                'script_url': f'/api/elevenlabs-script/{script_filename}',
                'audio_url': f'/api/elevenlabs-audio/{audio_filename}',
                'script_text': narration_script
            })
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
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