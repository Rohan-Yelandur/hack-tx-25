"""
Helper utilities for the backend.
Common functions used across different services.
"""

import os
import re
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_file_id(content: str) -> str:
    """
    Generate a unique file ID based on content hash.
    Useful for caching and avoiding duplicate processing.
    
    Args:
        content: String content to hash
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def clean_latex(text: str) -> str:
    """
    Clean and normalize LaTeX expressions in text.
    Ensures consistent formatting for rendering.
    
    Args:
        text: Text potentially containing LaTeX
        
    Returns:
        Cleaned text with normalized LaTeX
    """
    # Normalize inline math delimiters
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
    
    # Normalize display math delimiters
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_math_expressions(text: str) -> List[str]:
    """
    Extract all LaTeX math expressions from text.
    
    Args:
        text: Text containing LaTeX expressions
        
    Returns:
        List of extracted math expressions
    """
    # Extract inline math
    inline = re.findall(r'\$(.*?)\$', text)
    
    # Extract display math
    display = re.findall(r'\$\$(.*?)\$\$', text)
    
    return inline + display


def format_timestamp(seconds: float) -> str:
    """
    Format seconds into MM:SS or HH:MM:SS timestamp.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def parse_timestamp(timestamp: str) -> float:
    """
    Parse timestamp string into seconds.
    
    Args:
        timestamp: String in format MM:SS or HH:MM:SS
        
    Returns:
        Time in seconds
    """
    parts = timestamp.split(':')
    
    if len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    
    raise ValueError(f"Invalid timestamp format: {timestamp}")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystem use
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    
    return name + ext


def ensure_file_extension(filename: str, extension: str) -> str:
    """
    Ensure filename has the correct extension.
    
    Args:
        filename: Original filename
        extension: Desired extension (with or without dot)
        
    Returns:
        Filename with correct extension
    """
    if not extension.startswith('.'):
        extension = '.' + extension
    
    if not filename.endswith(extension):
        filename = os.path.splitext(filename)[0] + extension
    
    return filename


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """
    Remove files older than specified age from directory.
    
    Args:
        directory: Directory to clean
        max_age_hours: Maximum age in hours
        
    Returns:
        Number of files deleted
    """
    if not os.path.exists(directory):
        return 0
    
    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
    deleted_count = 0
    
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_modified < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.info(f"Deleted old file: {filename}")
    
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")
    
    return deleted_count


def validate_problem_text(text: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that problem text is appropriate and safe.
    
    Args:
        text: Problem text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Problem text cannot be empty"
    
    if len(text) < 10:
        return False, "Problem text too short (minimum 10 characters)"
    
    if len(text) > 10000:
        return False, "Problem text too long (maximum 10000 characters)"
    
    return True, None


def parse_scene_plan(scene_text: str) -> List[Dict]:
    """
    Parse scene plan text into structured format.
    Extracts scene descriptions for video generation.
    
    Args:
        scene_text: Raw scene plan text from LLM
        
    Returns:
        List of scene dictionaries
    """
    scenes = []
    
    # Try to extract structured sections
    # This is a simple parser - can be enhanced based on actual LLM output format
    lines = scene_text.split('\n')
    current_scene = None
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        # Detect scene headers (e.g., "Scene 1:", "## Scene 1")
        if re.match(r'^(Scene|##)\s*\d+', line, re.IGNORECASE):
            if current_scene:
                scenes.append(current_scene)
            
            current_scene = {
                'title': line,
                'visual_elements': [],
                'text': '',
                'timing': None
            }
        
        elif current_scene:
            # Look for timing information
            timing_match = re.search(r'(\d+:\d+)\s*-\s*(\d+:\d+)', line)
            if timing_match:
                current_scene['timing'] = {
                    'start': timing_match.group(1),
                    'end': timing_match.group(2)
                }
            
            # Extract LaTeX expressions as visual elements
            math_expressions = extract_math_expressions(line)
            if math_expressions:
                current_scene['visual_elements'].extend(math_expressions)
            
            # Accumulate text
            current_scene['text'] += ' ' + line
    
    # Add last scene
    if current_scene:
        scenes.append(current_scene)
    
    return scenes


def create_response(
    success: bool,
    message: str = "",
    data: Optional[Dict] = None,
    error: Optional[str] = None
) -> Dict:
    """
    Create standardized API response format.
    
    Args:
        success: Whether the operation succeeded
        message: Human-readable message
        data: Response data (for successful operations)
        error: Error message (for failed operations)
        
    Returns:
        Standardized response dictionary
    """
    response = {
        'success': success,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if data:
        response['data'] = data
    
    if error:
        response['error'] = error
    
    return response


def estimate_reading_time(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate how long it takes to read text aloud.
    
    Args:
        text: Text to estimate
        words_per_minute: Average speaking rate
        
    Returns:
        Estimated time in seconds
    """
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    return minutes * 60

