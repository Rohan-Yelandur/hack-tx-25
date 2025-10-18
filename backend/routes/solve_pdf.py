"""
PDF-based problem solving endpoint.
Handles PDF worksheet uploads and extraction.
"""

import logging
from flask import request, jsonify
from werkzeug.utils import secure_filename
from routes import api_bp
from services import get_orchestrator, get_audio_generator, get_video_generator, get_file_storage
from utils.helpers import create_response

logger = logging.getLogger(__name__)


@api_bp.route('/solve_pdf', methods=['POST'])
def solve_pdf():
    """
    Upload a PDF worksheet and generate explanations for contained problems.
    
    Request:
        Multipart form data with:
        - file: PDF file
        - generate_audio: boolean (optional, default true)
        - generate_video: boolean (optional, default true)
    
    Returns:
        JSON response with solutions, audio, and video URLs for each problem
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify(create_response(
                success=False,
                error="No file provided"
            )), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify(create_response(
                success=False,
                error="Empty filename"
            )), 400
        
        # Validate file extension
        if not file.filename.lower().endswith('.pdf'):
            return jsonify(create_response(
                success=False,
                error="File must be a PDF"
            )), 400
        
        # Parse options
        generate_audio = request.form.get('generate_audio', 'true').lower() == 'true'
        generate_video = request.form.get('generate_video', 'true').lower() == 'true'
        
        logger.info(f"Processing PDF: {file.filename}")
        
        # Initialize services
        file_storage = get_file_storage()
        orchestrator = get_orchestrator()
        
        # Save the PDF file
        file_info = file_storage.save_pdf(file)
        pdf_path = file_info['filepath']
        
        logger.info(f"PDF saved: {pdf_path}")
        
        # Process the PDF
        problems = orchestrator.process_pdf_problem(pdf_path)
        
        response_data = {
            'pdf_filename': file_info['original_filename'],
            'problems_count': len(problems),
            'problems': []
        }
        
        # Process each problem
        for i, problem_result in enumerate(problems):
            problem_data = {
                'problem_number': i + 1,
                'problem_text': problem_result['problem_text'],
                'solution': problem_result['solution'],
                'teaching_script': problem_result['teaching_script'],
                'estimated_duration': problem_result['estimated_duration']
            }
            
            # Generate audio if requested
            if generate_audio:
                try:
                    audio_gen = get_audio_generator()
                    audio_result = audio_gen.generate_audio_with_timestamps(
                        problem_result['teaching_script']
                    )
                    
                    audio_url = file_storage.get_audio_url(
                        audio_result['audio_filename'],
                        base_url=request.host_url
                    )
                    
                    problem_data['audio'] = {
                        'url': audio_url,
                        'filename': audio_result['audio_filename'],
                        'file_size': audio_result['file_size'],
                        'timestamps': audio_result.get('timestamps', [])
                    }
                    
                    logger.info(f"Audio generated for problem {i + 1}")
                    
                except Exception as e:
                    logger.error(f"Error generating audio for problem {i + 1}: {str(e)}")
                    problem_data['audio_error'] = str(e)
            
            # Generate video if requested
            if generate_video:
                try:
                    video_gen = get_video_generator()
                    
                    # Use audio if available
                    audio_path = None
                    timestamps = None
                    if generate_audio and 'audio' in problem_data:
                        audio_path = audio_result.get('audio_path')
                        timestamps = audio_result.get('timestamps')
                    
                    video_result = video_gen.generate_video(
                        script=problem_result['teaching_script'],
                        scene_plan=problem_result['scene_plan'],
                        audio_path=audio_path,
                        timestamps=timestamps
                    )
                    
                    video_url = file_storage.get_video_url(
                        video_result['video_filename'],
                        base_url=request.host_url
                    )
                    
                    problem_data['video'] = {
                        'url': video_url,
                        'filename': video_result['video_filename'],
                        'file_size': video_result['file_size']
                    }
                    
                    logger.info(f"Video generated for problem {i + 1}")
                    
                except Exception as e:
                    logger.error(f"Error generating video for problem {i + 1}: {str(e)}")
                    problem_data['video_error'] = str(e)
            
            response_data['problems'].append(problem_data)
        
        # Return successful response
        return jsonify(create_response(
            success=True,
            message=f"PDF processed successfully with {len(problems)} problem(s)",
            data=response_data
        )), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify(create_response(
            success=False,
            error=str(e)
        )), 400
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return jsonify(create_response(
            success=False,
            error=f"Internal server error: {str(e)}"
        )), 500


@api_bp.route('/solve_pdf/status', methods=['GET'])
def solve_pdf_status():
    """
    Check if the PDF solving service is available.
    
    Returns:
        JSON response with service status
    """
    try:
        return jsonify(create_response(
            success=True,
            message="PDF solving service is available",
            data={'status': 'ready'}
        )), 200
        
    except Exception as e:
        return jsonify(create_response(
            success=False,
            error=str(e)
        )), 500

