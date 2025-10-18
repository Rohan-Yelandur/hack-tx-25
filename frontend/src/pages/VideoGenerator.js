import { useState, useRef, useEffect } from 'react';
import { API_BASE_URL } from '../config/constants';
import './VideoGenerator.css';

function VideoGenerator() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');
  const [manimCode, setManimCode] = useState('');
  const [narrationScript, setNarrationScript] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [showContent, setShowContent] = useState(false);

  const videoRef = useRef(null);
  const audioRef = useRef(null);

  // Synchronize audio with video playback
  useEffect(() => {
    const video = videoRef.current;
    const audio = audioRef.current;

    // Skip sync if no audio URL or refs are missing
    if (!video || !audio || !audioUrl) return;

    const syncPlay = () => {
      if (audioUrl) {
        audio.currentTime = video.currentTime;
        audio.play().catch(err => console.log('Audio play failed:', err));
      }
    };

    const syncPause = () => {
      if (audioUrl) {
        audio.pause();
      }
    };

    const syncSeeking = () => {
      if (audioUrl) {
        audio.currentTime = video.currentTime;
      }
    };

    video.addEventListener('play', syncPlay);
    video.addEventListener('pause', syncPause);
    video.addEventListener('seeking', syncSeeking);

    return () => {
      video.removeEventListener('play', syncPlay);
      video.removeEventListener('pause', syncPause);
      video.removeEventListener('seeking', syncSeeking);
    };
  }, [showContent, audioUrl]);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError('');
    setVideoUrl('');
    setManimCode('');
    setNarrationScript('');
    setAudioUrl('');
    setShowContent(false);

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt
        }),
      });

      const data = await response.json();
      console.log('API Response:', data); // Debug log

      if (data.success) {
        // Show content even if only video is ready (audio is optional)
        if (data.video_url) {
          setVideoUrl(`${API_BASE_URL}${data.video_url}`);
          setManimCode(data.manim_code || '');
          setNarrationScript(data.script_text || '');
          setAudioUrl(data.audio_url ? `${API_BASE_URL}${data.audio_url}` : '');
          setShowContent(true);
          
          // Log warnings if audio failed
          if (!data.audio_url && data.audio_error) {
            console.warn('Audio generation failed:', data.audio_error);
          }
        } else {
          setError(data.video_error || 'Failed to generate video');
        }
      } else {
        setError(data.error || 'Failed to generate video');
      }
    } catch (err) {
      console.error('Fetch error:', err);
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
      {showContent && (
        <div className="video-section">
          <h2 className="section-title">Your Animation</h2>
          <div className="video-container">
            <video
              ref={videoRef}
              controls
              key={videoUrl}
              className="video-player"
            >
              <source src={videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            {/* Hidden audio element that syncs with video - only if audio exists */}
            {audioUrl && (
              <audio
                ref={audioRef}
                style={{ display: 'none' }}
                key={audioUrl}
              >
                <source src={audioUrl} type="audio/mpeg" />
              </audio>
            )}
          </div>

          {/* Narration Script Display */}
          {narrationScript && (
            <div className="audio-section">
              <h3 className="section-subtitle">AI Narration Script</h3>
              <div className="narration-script">
                <p className="script-text">{narrationScript}</p>
              </div>
            </div>
          )}

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
