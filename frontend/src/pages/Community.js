import React, { useState, useEffect, useRef } from 'react';
import './Community.css';
import { API_BASE_URL } from '../config/constants';

function Community() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const videoRefs = useRef({});

  useEffect(() => {
    fetchVideos();
  }, []);

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
                src={`${API_BASE_URL}${video.final_video_url}`}
              >
                Your browser does not support the video tag.
              </video>
            </div>

            <div className="video-info">
              <div className="video-meta">
                <span className="timestamp">
                  {formatDate(video.created_at)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Community;
