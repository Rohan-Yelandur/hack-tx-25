import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { API_BASE_URL } from '../config/constants';
import './VideoGenerator.css';

function VideoGenerator() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');
  const [manimCode, setManimCode] = useState('');
  const [narrationScript, setNarrationScript] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [showContent, setShowContent] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfPreview, setPdfPreview] = useState(null);

  const videoRef = useRef(null);
  const audioRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Synchronize audio with video playback
  useEffect(() => {
    const video = videoRef.current;
    const audio = audioRef.current;

    if (!video || !audio) return;

    const syncPlay = () => {
      audio.currentTime = video.currentTime;
      audio.play();
    };

    const syncPause = () => {
      audio.pause();
    };

    const syncSeeking = () => {
      audio.currentTime = video.currentTime;
    };

    video.addEventListener('play', syncPlay);
    video.addEventListener('pause', syncPause);
    video.addEventListener('seeking', syncSeeking);

    return () => {
      video.removeEventListener('play', syncPlay);
      video.removeEventListener('pause', syncPause);
      video.removeEventListener('seeking', syncSeeking);
    };
  }, [showContent]);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, [prompt]);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      setPdfPreview({
        name: file.name,
        size: (file.size / 1024).toFixed(2) + ' KB'
      });
    } else if (file) {
      setError('Please select a PDF file only');
      setPdfFile(null);
      setPdfPreview(null);
    }
  };

  const handleRemovePdf = () => {
    setPdfFile(null);
    setPdfPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

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
      const formData = new FormData();
      formData.append('prompt', prompt);
      if (pdfFile) {
        formData.append('pdf', pdfFile);
      }

      const response = await fetch(`${API_BASE_URL}/api/generate-video`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        // Only show content when BOTH video and audio are ready
        if (data.video_url && data.audio_url) {
          setVideoUrl(`${API_BASE_URL}${data.video_url}`);
          setManimCode(data.manim_code);
          setNarrationScript(data.script_text);
          setAudioUrl(`${API_BASE_URL}${data.audio_url}`);
          setShowContent(true);
        } else {
          setError('Video or audio generation incomplete');
        }
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
        
        <div className="input-container">
          <motion.div 
            className="chat-input-wrapper"
            initial={{ height: 'auto' }}
            animate={{ height: 'auto' }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
          >
            <textarea
              ref={textareaRef}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask a question or describe what you'd like to learn..."
              disabled={loading}
              className="chat-input"
              rows="1"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleGenerate();
                }
              }}
            />
            
            <div className="input-controls">
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
              
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
                className="attach-btn celestial-btn"
                title="Attach PDF"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                </svg>
              </button>
              
              <button
                onClick={handleGenerate}
                disabled={loading || !prompt.trim()}
                className="send-btn celestial-btn"
                title="Generate Animation"
              >
                {loading ? (
                  <div className="btn-spinner"></div>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                  </svg>
                )}
              </button>
            </div>
          </motion.div>

          {/* PDF Preview */}
          {pdfPreview && (
            <motion.div 
              className="pdf-preview"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              <div className="pdf-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <text x="8" y="16" fontSize="6" fill="currentColor">PDF</text>
                </svg>
              </div>
              <div className="pdf-info">
                <div className="pdf-name">{pdfPreview.name}</div>
                <div className="pdf-size">{pdfPreview.size}</div>
              </div>
              <button onClick={handleRemovePdf} className="pdf-remove" title="Remove PDF">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </motion.div>
          )}
        </div>
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
            {/* Hidden audio element that syncs with video */}
            <audio
              ref={audioRef}
              style={{ display: 'none' }}
              key={audioUrl}
            >
              <source src={audioUrl} type="audio/mpeg" />
            </audio>
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

          {/* {manimCode && (
            <details className="code-section">
              <summary className="code-summary">View Generated Code</summary>
              <pre className="code-block">{manimCode}</pre>
            </details>
          )} */}
        </div>
      )}
    </div>
  );
}

export default VideoGenerator;
