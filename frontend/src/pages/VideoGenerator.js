import { useState } from 'react';
import { API_BASE_URL } from '../config/constants';
import './VideoGenerator.css';

function VideoGenerator() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');
  const [manimCode, setManimCode] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError('');
    setVideoUrl('');
    setManimCode('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();

      if (data.success) {
        setVideoUrl(`${API_BASE_URL}${data.video_url}`);
        setManimCode(data.manim_code);
      } else {
        setError(data.error || 'Failed to generate video');
      }
    } catch (err) {
      setError('Failed to connect to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="video-generator">
      {/* Input Section */}
      <div className="input-section">
        <h2 className="input-title">
          Generate <span className="highlight-cyan">Animations</span> with AI
        </h2>
        <div className="form-group">
          <label htmlFor="prompt">Describe Your Animation</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Visualize the Pythagorean theorem with rotating triangles..."
            rows="5"
            disabled={loading}
            className="prompt-input"
          />
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="generate-btn"
        >
          {loading ? 'Generating...' : 'Generate Video'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="message-card error-message">
          <div className="message-icon">✕</div>
          <p>{error}</p>
        </div>
      )}

      {/* Loading Message */}
      {loading && (
        <div className="message-card loading-message">
          <div className="loading-spinner"></div>
          <p>Generating your animation... This may take a minute.</p>
        </div>
      )}

      {/* Video Section */}
      {videoUrl && (
        <div className="video-section">
          <h2 className="section-title">Your Animation</h2>
          <div className="video-container">
            <video
              controls
              autoPlay
              loop
              key={videoUrl}
              className="video-player"
            >
              <source src={videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>

          {manimCode && (
            <details className="code-section">
              <summary className="code-summary">View Generated Code</summary>
              <pre className="code-block">{manimCode}</pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
}

export default VideoGenerator;
