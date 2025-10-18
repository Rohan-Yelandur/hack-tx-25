"""
Text-based problem solving endpoint.
Handles POST requests with text math problems.
"""

import logging
from flask import request, jsonify, url_for
from routes import api_bp
from services import get_orchestrator, get_audio_generator, get_video_generator, get_file_storage
from utils.helpers import create_response, validate_problem_text

logger = logging.getLogger(__name__)


@api_bp.route('/solve_text', methods=['POST'])
def solve_text():
    """
    Solve a text-based math problem and generate explanation.
    
    Request Body:
        {
            "problem": "string - the math problem to solve",
            "generate_audio": "boolean - optional, default true",
            "generate_video": "boolean - optional, default true"
        }
    
    Returns:
        JSON response with solution, audio, and video URLs
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify(create_response(
                success=False,
                error="No JSON data provided"
            )), 400
        
        problem_text = data.get('problem', '').strip()
        generate_audio = data.get('generate_audio', True)
        generate_video = data.get('generate_video', True)
        
        # Validate problem text
        is_valid, error_msg = validate_problem_text(problem_text)
        if not is_valid:
            return jsonify(create_response(
                success=False,
                error=error_msg
            )), 400
        
        logger.info(f"Processing text problem: {problem_text[:100]}...")
        
        # Initialize services
        orchestrator = get_orchestrator()
        file_storage = get_file_storage()
        
        # Step 1: Process the problem (analysis, solution, teaching script, scene plan)
        result = orchestrator.process_problem(problem_text)
        
        response_data = {
            'problem': result['problem_text'],
            'solution': result['solution'],
            'teaching_script': result['teaching_script'],
            'estimated_duration': result['estimated_duration']
        }
        
        # Step 2: Generate audio if requested
        if generate_audio:
            try:
                audio_gen = get_audio_generator()
                audio_result = audio_gen.generate_audio_with_timestamps(
                    result['teaching_script']
                )
                
                # Generate URL for audio
                audio_url = file_storage.get_audio_url(
                    audio_result['audio_filename'],
                    base_url=request.host_url
                )
                
                response_data['audio'] = {
                    'url': audio_url,
                    'filename': audio_result['audio_filename'],
                    'file_size': audio_result['file_size'],
                    'timestamps': audio_result.get('timestamps', [])
                }
                
                logger.info("Audio generated successfully")
                
            except Exception as e:
                logger.error(f"Error generating audio: {str(e)}")
                response_data['audio_error'] = str(e)
        
        # Step 3: Generate video if requested
        if generate_video:
            try:
                video_gen = get_video_generator()
                
                # Use audio if available
                audio_path = None
                timestamps = None
                if generate_audio and 'audio' in response_data:
                    audio_path = audio_result.get('audio_path')
                    timestamps = audio_result.get('timestamps')
                
                video_result = video_gen.generate_video(
                    script=result['teaching_script'],
                    scene_plan=result['scene_plan'],
                    audio_path=audio_path,
                    timestamps=timestamps
                )
                
                # Generate URL for video
                video_url = file_storage.get_video_url(
                    video_result['video_filename'],
                    base_url=request.host_url
                )
                
                response_data['video'] = {
                    'url': video_url,
                    'filename': video_result['video_filename'],
                    'file_size': video_result['file_size']
                }
                
                logger.info("Video generated successfully")
                
            except Exception as e:
                logger.error(f"Error generating video: {str(e)}")
                response_data['video_error'] = str(e)
        
        # Return successful response
        return jsonify(create_response(
            success=True,
            message="Problem solved successfully",
            data=response_data
        )), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify(create_response(
            success=False,
            error=str(e)
        )), 400
        
    except Exception as e:
        logger.error(f"Error processing text problem: {str(e)}")
        return jsonify(create_response(
            success=False,
            error=f"Internal server error: {str(e)}"
        )), 500


@api_bp.route('/solve_text/status', methods=['GET'])
def solve_text_status():
    """
    Check if the text solving service is available.
    
    Returns:
        JSON response with service status
    """
    try:
        return jsonify(create_response(
            success=True,
            message="Text solving service is available",
            data={'status': 'ready'}
        )), 200
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            error=str(e)
        )), 500

