from flask import request, jsonify, send_file
from pathlib import Path
from gemini_service import gemini_service
from elevenlabs_service import eleven_labs_service
from manim_service import manim_service


def register_routes(app):
    """Register all API routes with the Flask app."""
    
    @app.route('/api/generate-video', methods=['POST'])
    def generate_video():
        """Generate a complete video with narration from a prompt."""
        data = request.json
        prompt = data.get('prompt', '')
        generate_audio = data.get('generate_audio', False)
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        try:
            # Generate Manim code
            manim_code = gemini_service.generate_manim_code(prompt)
            
            # Render video
            video_path, script_path = manim_service.render_manim_video(manim_code)
            
            if not video_path:
                return jsonify({
                    'success': False,
                    'error': 'Failed to render video',
                    'manim_script_url': f'/api/manim-code/{Path(script_path).name}'
                }), 500
            
            video_filename = Path(video_path).name
            manim_script_filename = Path(script_path).name
            
            response_data = {
                'success': True,
                'video_url': f'/api/manim-video/{video_filename}',
                'manim_code_url': f'/api/manim-code/{manim_script_filename}',
                'manim_code': manim_code
            }
            
            # Optionally generate narration
            if generate_audio:
                audio_path, script_path, narration_script = eleven_labs_service.generate_audio_from_prompt(prompt)
                
                if audio_path:
                    audio_filename = Path(audio_path).name
                    script_filename = Path(script_path).name
                    response_data['narration_script_url'] = f'/api/elevenlabs-script/{script_filename}'
                    response_data['narration_audio_url'] = f'/api/elevenlabs-audio/{audio_filename}'
                    response_data['narration_script'] = narration_script
            
            return jsonify(response_data)
            
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
            # Generate script and audio
            audio_path, script_path, narration_script = eleven_labs_service.generate_audio_from_prompt(prompt)
            
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