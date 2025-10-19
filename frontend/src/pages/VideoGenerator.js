import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { API_BASE_URL } from '../config/constants';
import { useLessonContext } from '../context/LessonContext';
import './VideoGenerator.css';
import ConstellationLoading from '../components/ConstellationLoading';

function VideoGenerator() {
  const { currentLesson, updateLesson, clearLesson, setLoading: setContextLoading } = useLessonContext();
  
  const [prompt, setPrompt] = useState(currentLesson.prompt || '');
  const [error, setError] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfPreview, setPdfPreview] = useState(null);
  const [sharingLoading, setSharingLoading] = useState(false);
  const [tags, setTags] = useState([]);
  const [tagInput, setTagInput] = useState('');

  const videoRef = useRef(null);
  const inputSectionRef = useRef(null);
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

  // Smooth scroll helper (duration in ms)
  const smoothScrollTo = (targetY, duration = 600) => {
    const startY = window.scrollY || window.pageYOffset;
    const diff = targetY - startY;
    let start;

    const easeInOutCubic = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

    const step = (timestamp) => {
      if (!start) start = timestamp;
      const elapsed = timestamp - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeInOutCubic(progress);
      window.scrollTo(0, startY + diff * eased);
      if (elapsed < duration) {
        window.requestAnimationFrame(step);
      }
    };

    window.requestAnimationFrame(step);
  };

  // Scroll to input section when arrow clicked (smooth animation)
  const scrollToInput = () => {
    if (inputSectionRef.current) {
      const rect = inputSectionRef.current.getBoundingClientRect();
      const targetY = rect.top + window.pageYOffset - 20; // small offset
      smoothScrollTo(targetY, 650);
    }
  };

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

  const handleDownload = async () => {
    if (!videoId) {
      setError('No video to download');
      return;
    }

    try {
      // Use the new download endpoint that merges video and audio
      const downloadUrl = `${API_BASE_URL}/api/download-video/${videoId}`;

      // Create a temporary link and trigger download
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `animation_${videoId}.mp4`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download video: ' + err.message);
    }
  };

  const handleAddTag = (e) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault();
      const newTag = tagInput.trim().toLowerCase();
      if (!tags.includes(newTag) && tags.length < 5) {
        setTags([...tags, newTag]);
        setTagInput('');
      }
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
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
        body: JSON.stringify({
          tags: tags
        }),
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
<<<<<<< HEAD
    setVideoUrl('');
    setManimCode('');
    setNarrationScript('');
    setAudioUrl('');
    setShowContent(false);
    setVideoId('');
    setSharedToCommunity(false);
    setTags([]);
    setTagInput('');
=======
>>>>>>> 540152b405d4123081d56b0df595c17bb0d9f7cc

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

        <button className="hero-down" onClick={scrollToInput} aria-label="Scroll to generator">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="19 12 12 19 5 12"></polyline>
          </svg>
        </button>
      </div>

      {/* Input Section */}
  <div className="input-section" ref={inputSectionRef}>
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
          <ConstellationLoading />
        </div>
      )}

      {/* Video Section */}
      {currentLesson.hasContent && (
        <div className="video-section">
<<<<<<< HEAD
          <h2 className="section-title">Your Animation</h2>

          {/* Action Buttons */}
          <div className="action-buttons">
            {/* Download Button */}
            <button
              onClick={handleDownload}
              className="download-btn"
              title="Download video"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              Download
            </button>

            {/* Share to Community Button */}
            {videoId && (
              <div className="share-section">
                {!sharedToCommunity ? (
                  <div className="share-container">
                    {/* Tag Input */}
                    <div className="tag-input-section">
                      <label className="tag-label">Add tags (optional, max 5):</label>
                      <div className="tag-input-wrapper">
                        <input
                          type="text"
                          value={tagInput}
                          onChange={(e) => setTagInput(e.target.value)}
                          onKeyDown={handleAddTag}
                          placeholder="e.g., math, physics, tutorial"
                          className="tag-input"
                          maxLength={20}
                          disabled={tags.length >= 5}
                        />
                        {tags.length < 5 && (
                          <small className="tag-hint">Press Enter to add tag</small>
                        )}
                      </div>
                      {/* Tag Display */}
                      {tags.length > 0 && (
                        <div className="tags-display">
                          {tags.map((tag, index) => (
                            <span key={index} className="tag-pill">
                              {tag}
                              <button
                                onClick={() => handleRemoveTag(tag)}
                                className="tag-remove"
                                aria-label="Remove tag"
                              >
                                ×
                              </button>
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <button
                      onClick={handleShareToCommunity}
                      disabled={sharingLoading}
                      className="share-btn"
                    >
                      {sharingLoading ? 'Sharing...' : '✨ Share to Community'}
                    </button>
                  </div>
                ) : (
                  <div className="shared-message">
                    ✓ Shared to Community Gallery!
                  </div>
                )}
              </div>
            )}
=======
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
>>>>>>> 540152b405d4123081d56b0df595c17bb0d9f7cc
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
