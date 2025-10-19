import React, { useState, useEffect, useRef } from 'react';
import './Community.css';
import { API_BASE_URL } from '../config/constants';

function Community() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedCode, setExpandedCode] = useState({});
  const videoRefs = useRef({});
  const audioRefs = useRef({});

  useEffect(() => {
    fetchVideos();
  }, []);

  // Sync audio with video for a specific video ID
  useEffect(() => {
    videos.forEach((video) => {
      if (!video.audio_url) return;

      const videoElement = videoRefs.current[video.id];
      const audioElement = audioRefs.current[video.id];

      if (!videoElement || !audioElement) return;

      const handlePlay = () => {
        audioElement.currentTime = videoElement.currentTime;
        audioElement.play().catch(err => console.log('Audio play error:', err));
      };

      const handlePause = () => {
        audioElement.pause();
      };

      const handleSeeking = () => {
        audioElement.currentTime = videoElement.currentTime;
      };

      videoElement.addEventListener('play', handlePlay);
      videoElement.addEventListener('pause', handlePause);
      videoElement.addEventListener('seeking', handleSeeking);

      return () => {
        videoElement.removeEventListener('play', handlePlay);
        videoElement.removeEventListener('pause', handlePause);
        videoElement.removeEventListener('seeking', handleSeeking);
      };
    });
  }, [videos]);

  const fetchVideos = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await fetch(`${API_BASE_URL}/api/videos`);
      const data = await response.json();

      if (data.success) {
        setVideos(data.videos);
      } else {
        setError(data.error || 'Failed to load videos');
      }
    } catch (err) {
      setError('Failed to connect to server');
      console.error('Error fetching videos:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleCode = (videoId) => {
    setExpandedCode(prev => ({
      ...prev,
      [videoId]: !prev[videoId]
    }));
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="community-container">
      <div className="community-header">
        <h1>Community Gallery</h1>
        <p>Explore all generated animation videos</p>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading videos...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={fetchVideos} className="retry-button">Retry</button>
        </div>
      )}

      {!loading && !error && videos.length === 0 && (
        <div className="empty-state">
          <p>No videos generated yet.</p>
          <p>Go to the home page to create your first animation!</p>
        </div>
      )}

      <div className="videos-grid">
        {videos.map((video) => (
          <div key={video.id} className="video-card">
            <div className="video-player-container">
              <video
                ref={(el) => (videoRefs.current[video.id] = el)}
                controls
                className="video-player"
                src={`${API_BASE_URL}${video.video_url}`}
              >
                Your browser does not support the video tag.
              </video>
              {video.audio_url && (
                <audio
                  ref={(el) => (audioRefs.current[video.id] = el)}
                  id={`audio-${video.id}`}
                  src={`${API_BASE_URL}${video.audio_url}`}
                  style={{ display: 'none' }}
                />
              )}
            </div>

            <div className="video-info">
              {video.script_text && (
                <div className="script-preview">
                  <h3>Narration</h3>
                  <p>{video.script_text}</p>
                </div>
              )}

              <div className="video-meta">
                <span className="timestamp">
                  {formatDate(video.created_at)}
                </span>
              </div>

              {video.manim_code_url && (
                <div className="code-section">
                  <button
                    onClick={() => toggleCode(video.id)}
                    className="toggle-code-button"
                  >
                    {expandedCode[video.id] ? 'Hide Code' : 'View Code'}
                  </button>

                  {expandedCode[video.id] && (
                    <div className="code-container">
                      <a
                        href={`${API_BASE_URL}${video.manim_code_url}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="view-code-link"
                      >
                        Open Code File →
                      </a>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Community;
