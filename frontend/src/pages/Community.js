import React, { useState, useEffect, useRef } from 'react';
import './Community.css';
import { API_BASE_URL } from '../config/constants';

function Community() {
  const [videos, setVideos] = useState([]);
  const [filteredVideos, setFilteredVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState([]);
  const [expandedCode, setExpandedCode] = useState({});
  const [selectedTags, setSelectedTags] = useState([]);
  const [availableTags, setAvailableTags] = useState([]);
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
        setFilteredVideos(data.videos);

        // Extract all unique tags from videos
        const tags = new Set();
        data.videos.forEach(video => {
          if (video.tags && Array.isArray(video.tags)) {
            video.tags.forEach(tag => tags.add(tag));
          }
        });
        setAvailableTags(Array.from(tags).sort());
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

  // Filter videos when selected tags change
  useEffect(() => {
    if (selectedTags.length === 0) {
      setFilteredVideos(videos);
    } else {
      const filtered = videos.filter(video => {
        if (!video.tags || video.tags.length === 0) return false;
        // Video must have at least one of the selected tags
        return selectedTags.some(tag => video.tags.includes(tag));
      });
      setFilteredVideos(filtered);
    }
  }, [selectedTags, videos]);

  const toggleTag = (tag) => {
    setSelectedTags(prev => {
      if (prev.includes(tag)) {
        return prev.filter(t => t !== tag);
      } else {
        return [...prev, tag];
      }
    });
  };

  const clearFilters = () => {
    setSelectedTags([]);
  };

  const handleDownload = async (videoId) => {
    // Videos already have audio embedded (final_video_url)
    const video = videos.find(v => v.id === videoId);
    if (video && video.final_video_url) {
      try {
        const downloadUrl = `${API_BASE_URL}${video.final_video_url}`;

        // Fetch the video as a blob to force download instead of navigation
        const response = await fetch(downloadUrl);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `animation_${videoId}.mp4`;
        document.body.appendChild(a);
        a.click();

        // Clean up
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } catch (err) {
        console.error('Download failed:', err);
      }
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

      {/* Tag Filters */}
      {!loading && !error && availableTags.length > 0 && (
        <div className="filters-section">
          <div className="filters-header">
            <h3>Filter by Tags:</h3>
            {selectedTags.length > 0 && (
              <button onClick={clearFilters} className="clear-filters-btn">
                Clear Filters
              </button>
            )}
          </div>
          <div className="tag-filters">
            {availableTags.map((tag) => (
              <button
                key={tag}
                onClick={() => toggleTag(tag)}
                className={`filter-tag ${selectedTags.includes(tag) ? 'active' : ''}`}
              >
                {tag}
              </button>
            ))}
          </div>
          {selectedTags.length > 0 && (
            <p className="filter-results">
              Showing {filteredVideos.length} of {videos.length} videos
            </p>
          )}
        </div>
      )}

      {!loading && !error && filteredVideos.length === 0 && videos.length > 0 && (
        <div className="empty-state">
          <p>No videos match the selected tags.</p>
          <button onClick={clearFilters} className="clear-filters-btn">
            Clear Filters
          </button>
        </div>
      )}

      <div className="videos-grid">
        {filteredVideos.map((video) => (
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
              {video.script_text && (
                <div className="script-preview">
                  <h3>Narration</h3>
                  <p>{video.script_text}</p>
                </div>
              )}

              {/* Display video tags */}
              {video.tags && video.tags.length > 0 && (
                <div className="video-tags">
                  {video.tags.map((tag, index) => (
                    <span key={index} className="video-tag">
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              <div className="video-meta">
                <span className="timestamp">
                  {formatDate(video.created_at)}
                </span>
                <button
                  onClick={() => handleDownload(video.id)}
                  className="download-video-btn"
                  title="Download video with audio"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                </button>
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
