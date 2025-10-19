import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { API_BASE_URL } from '../config/constants';
import { useLessonContext } from '../context/LessonContext';
import './VideoGenerator.css';

function VideoGenerator() {
  const { currentLesson, updateLesson, clearLesson, setLoading: setContextLoading } = useLessonContext();
  
  const [prompt, setPrompt] = useState(currentLesson.prompt || '');
  const [error, setError] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfPreview, setPdfPreview] = useState(null);
  const [sharingLoading, setSharingLoading] = useState(false);

  const videoRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Get loading state from context
  const loading = currentLesson.loading;

  // Initialize from context when component mounts
  useEffect(() => {
    if (currentLesson.hasContent) {
      setPrompt(currentLesson.prompt);
    }
  }, [currentLesson.hasContent, currentLesson.prompt]);

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

  const handleShareToCommunity = async () => {
    if (!currentLesson.videoId) {
      setError('No video to share');
      return;
    }

    setSharingLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/videos/${currentLesson.videoId}/share-to-community`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (data.success) {
        updateLesson({ sharedToCommunity: true });
      } else {
        setError(data.error || 'Failed to share video');
      }
    } catch (err) {
      setError('Failed to connect to server: ' + err.message);
    } finally {
      setSharingLoading(false);
    }
  };

  const handleNewLesson = () => {
    clearLesson();
    setPrompt('');
    setError('');
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

    setContextLoading(true);
    setError('');

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
      console.log('API Response:', data); // Debug log

      if (data.success) {
        // Use the final combined video with embedded audio
        if (data.final_video_url) {
          // Update the lesson context with new data
          updateLesson({
            prompt: prompt,
            videoUrl: `${API_BASE_URL}${data.final_video_url}`,
            narrationScript: data.script_text || '',
            videoId: data.video_id || '',
            sharedToCommunity: false,
            loading: false,
          });
        } else {
          setError(data.video_error || data.audio_error || 'Failed to generate video');
        }
      } else {
        setError(data.error || 'Failed to generate video');
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError('Failed to connect to server: ' + err.message);
    } finally {
      setContextLoading(false);
    }
  };

  return (
    <div className="video-generator">
      {/* Hero Section */}
      <div className="hero-section">
        <h1 className="hero-title">Canopus</h1>
        <p className="hero-subtitle">We Help You Connect the Dots</p>
      </div>

      {/* Input Section */}
      <div className="input-section">
        <h2 className="input-title">
          Generate <span className="highlight-cyan">Lessons</span> with AI
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
      {currentLesson.hasContent && (
        <div className="video-section">
          <div className="section-header">
            <h2 className="section-title">Your Animation</h2>
            <div className="header-buttons">
              {currentLesson.videoId && !currentLesson.sharedToCommunity && (
                <button
                  onClick={handleShareToCommunity}
                  disabled={sharingLoading}
                  className="share-btn celestial-btn"
                  title="Share to Community"
                >
                  {sharingLoading ? (
                    <div className="btn-spinner"></div>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/>
                    </svg>
                  )}
                </button>
              )}
              {currentLesson.videoId && currentLesson.sharedToCommunity && (
                <div className="shared-indicator" title="Shared to Community">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              )}
              <button
                onClick={handleNewLesson}
                className="new-lesson-btn celestial-btn"
                title="Start a new lesson"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="12" y1="18" x2="12" y2="12"></line>
                  <line x1="9" y1="15" x2="15" y2="15"></line>
                </svg>
              </button>
            </div>
          </div>

          <div className="video-container">
            <video
              ref={videoRef}
              controls
              key={currentLesson.videoUrl}
              className="video-player"
            >
              <source src={currentLesson.videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      )}
    </div>
  );
}

export default VideoGenerator;
