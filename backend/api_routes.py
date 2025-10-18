from flask import request, jsonify, send_file
from pathlib import Path
from gemini_service import gemini_service
from manim_service import manim_service


def register_routes(app):
    """Register all API routes with the Flask app."""
    
    @app.route('/api/generate', methods=['POST'])
    def generate_video():
        """API endpoint to generate a video from a prompt."""
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        try:
            manim_code = gemini_service.generate_manim_code(prompt)
            video_path, script_path = manim_service.render_manim_video(manim_code)
            
            if video_path:
                video_filename = Path(video_path).name
                script_filename = Path(script_path).name
                
                return jsonify({
                    'success': True,
                    'video_url': f'/api/video/{video_filename}',
                    'script_url': f'/api/script/{script_filename}',
                    'manim_code': manim_code
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to render video',
                    'script_url': f'/api/script/{Path(script_path).name}'
                }), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/video/<filename>', methods=['GET'])
    def get_video(filename):
        """Serve video files."""
        video_path = manim_service.get_video_path(filename)
        if video_path.exists():
            return send_file(video_path, mimetype='video/mp4')
        return jsonify({'error': 'Video not found'}), 404
    
    
    @app.route('/api/script/<filename>', methods=['GET'])
    def get_script(filename):
        """Serve script files."""
        script_path = manim_service.get_script_path(filename)
        if script_path.exists():
            return send_file(script_path, mimetype='text/plain')
        return jsonify({'error': 'Script not found'}), 404

