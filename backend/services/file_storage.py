"""
File Storage Service.
Handles file uploads, storage, retrieval, and cleanup.
"""

import os
import shutil
import logging
from datetime import datetime
from typing import Dict, Optional, List
from werkzeug.utils import secure_filename
from config import Config
from utils.helpers import (
    sanitize_filename,
    generate_file_id,
    cleanup_old_files
)

logger = logging.getLogger(__name__)


class FileStorage:
    """
    Manages file storage for uploads, audio, and video files.
    Provides methods for saving, retrieving, and cleaning up files.
    """
    
    def __init__(self):
        """Initialize file storage with configuration."""
        Config.ensure_directories()
        
        self.upload_folder = Config.UPLOAD_FOLDER
        self.audio_folder = Config.AUDIO_FOLDER
        self.video_folder = Config.VIDEO_FOLDER
        self.static_folder = Config.STATIC_FOLDER
        
        logger.info("File storage initialized")
    
    def save_upload(self, file, custom_filename: Optional[str] = None) -> Dict:
        """
        Save an uploaded file to the upload directory.
        
        Args:
            file: File object from Flask request
            custom_filename: Optional custom filename
            
        Returns:
            Dictionary containing file information
            
        Raises:
            ValueError: If file is invalid
            Exception: If save fails
        """
        try:
            # Validate file
            if not file:
                raise ValueError("No file provided")
            
            if not file.filename:
                raise ValueError("File has no filename")
            
            # Determine filename
            if custom_filename:
                filename = secure_filename(custom_filename)
            else:
                filename = secure_filename(file.filename)
            
            filename = sanitize_filename(filename)
            
            # Generate unique filename to avoid collisions
            file_id = generate_file_id(f"{filename}_{datetime.now().isoformat()}")
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{file_id}{ext}"
            
            # Save file
            filepath = os.path.join(self.upload_folder, unique_filename)
            file.save(filepath)
            
            # Get file metadata
            file_size = os.path.getsize(filepath)
            
            result = {
                'filepath': filepath,
                'filename': unique_filename,
                'original_filename': file.filename,
                'file_size': file_size,
                'upload_time': datetime.now().isoformat()
            }
            
            logger.info(f"File saved: {unique_filename} ({file_size} bytes)")
            return result
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise Exception(f"Failed to save file: {str(e)}")
    
    def save_pdf(self, file) -> Dict:
        """
        Save a PDF file specifically for problem extraction.
        
        Args:
            file: PDF file object from Flask request
            
        Returns:
            Dictionary containing file information
            
        Raises:
            ValueError: If file is not a PDF
            Exception: If save fails
        """
        # Validate PDF
        if not file.filename.lower().endswith('.pdf'):
            raise ValueError("File must be a PDF")
        
        return self.save_upload(file)
    
    def get_file_url(self, filepath: str, base_url: str = '') -> str:
        """
        Generate a URL for accessing a file.
        
        Args:
            filepath: Absolute path to the file
            base_url: Base URL of the application
            
        Returns:
            Relative or absolute URL to the file
        """
        # Get relative path from static folder
        try:
            rel_path = os.path.relpath(filepath, Config.STATIC_FOLDER)
            url = f"/static/{rel_path}".replace('\\', '/')
            
            if base_url:
                url = f"{base_url.rstrip('/')}{url}"
            
            return url
            
        except Exception as e:
            logger.error(f"Error generating file URL: {str(e)}")
            return ""
    
    def get_audio_url(self, audio_filename: str, base_url: str = '') -> str:
        """
        Generate URL for an audio file.
        
        Args:
            audio_filename: Name of the audio file
            base_url: Base URL of the application
            
        Returns:
            URL to the audio file
        """
        url = f"/static/audio/{audio_filename}"
        
        if base_url:
            url = f"{base_url.rstrip('/')}{url}"
        
        return url
    
    def get_video_url(self, video_filename: str, base_url: str = '') -> str:
        """
        Generate URL for a video file.
        
        Args:
            video_filename: Name of the video file
            base_url: Base URL of the application
            
        Returns:
            URL to the video file
        """
        url = f"/static/videos/{video_filename}"
        
        if base_url:
            url = f"{base_url.rstrip('/')}{url}"
        
        return url
    
    def file_exists(self, filepath: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            filepath: Path to the file
            
        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(filepath) and os.path.isfile(filepath)
    
    def get_file_info(self, filepath: str) -> Optional[Dict]:
        """
        Get information about a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with file information, or None if file doesn't exist
        """
        if not self.file_exists(filepath):
            return None
        
        try:
            stat = os.stat(filepath)
            
            return {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'file_size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return None
    
    def delete_file(self, filepath: str) -> bool:
        """
        Delete a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            True if deletion succeeded, False otherwise
        """
        try:
            if self.file_exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted file: {filepath}")
                return True
            else:
                logger.warning(f"File not found for deletion: {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def cleanup_old_files(self) -> Dict[str, int]:
        """
        Clean up old files from all storage directories.
        Uses the retention period from configuration.
        
        Returns:
            Dictionary with cleanup statistics
        """
        logger.info("Starting file cleanup...")
        
        max_age = Config.FILE_RETENTION_HOURS
        
        stats = {
            'uploads_deleted': cleanup_old_files(self.upload_folder, max_age),
            'audio_deleted': cleanup_old_files(self.audio_folder, max_age),
            'videos_deleted': cleanup_old_files(self.video_folder, max_age)
        }
        
        total_deleted = sum(stats.values())
        logger.info(f"Cleanup complete: {total_deleted} files deleted")
        
        return stats
    
    def list_files(self, directory: str) -> List[Dict]:
        """
        List all files in a directory with their information.
        
        Args:
            directory: Directory to list
            
        Returns:
            List of file information dictionaries
        """
        files = []
        
        try:
            if not os.path.exists(directory):
                return files
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    file_info = self.get_file_info(filepath)
                    if file_info:
                        files.append(file_info)
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
        
        return files
    
    def get_storage_stats(self) -> Dict:
        """
        Get statistics about file storage usage.
        
        Returns:
            Dictionary with storage statistics
        """
        def get_directory_size(directory: str) -> int:
            """Calculate total size of all files in directory."""
            total = 0
            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        total += os.path.getsize(filepath)
            except Exception:
                pass
            return total
        
        def count_files(directory: str) -> int:
            """Count files in directory."""
            try:
                return len([f for f in os.listdir(directory) 
                           if os.path.isfile(os.path.join(directory, f))])
            except Exception:
                return 0
        
        return {
            'uploads': {
                'count': count_files(self.upload_folder),
                'size_bytes': get_directory_size(self.upload_folder)
            },
            'audio': {
                'count': count_files(self.audio_folder),
                'size_bytes': get_directory_size(self.audio_folder)
            },
            'videos': {
                'count': count_files(self.video_folder),
                'size_bytes': get_directory_size(self.video_folder)
            }
        }


def get_file_storage() -> FileStorage:
    """
    Factory function to get a file storage instance.
    
    Returns:
        Configured FileStorage instance
    """
    return FileStorage()

