import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { API_BASE_URL } from '../config/constants';
import { useLessonContext } from '../context/LessonContext';
import QuizContainer from '../components/Quiz/QuizContainer';
import ConstellationLoading from '../components/ConstellationLoading';
import './VideoGenerator.css';

function VideoGenerator({ showSplash }) {
  const { currentLesson, updateLesson, clearLesson } = useLessonContext();

  const [prompt, setPrompt] = useState(currentLesson.prompt || '');
  const [error, setError] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfPreview, setPdfPreview] = useState(null);
  const [sharingLoading, setSharingLoading] = useState(false);
  const [tags, setTags] = useState([]);
  const [tagInput, setTagInput] = useState('');

  // Separate loading and data states for video and quiz
  const [videoLoading, setVideoLoading] = useState(false);
  const [quizLoading, setQuizLoading] = useState(false);
  const [videoData, setVideoData] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [quizId, setQuizId] = useState(null);

  const videoRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

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

  const handleDownload = async () => {
    const videoId = videoData?.videoId || currentLesson.videoId;
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
    const videoId = videoData?.videoId || currentLesson.videoId;
    if (!videoId) {
      setError('No video to share');
      return;
    }

    setSharingLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/videos/${videoId}/share-to-community`, {
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
    setVideoData(null);
    setQuizData(null);
    setQuizId(null);
    setTags([]);
    setTagInput('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    // Reset states and start loading
    setError('');
    clearLesson();
    setTags([]);
    setTagInput('');
    setVideoData(null);
    setQuizData(null);
    setQuizId(null);
    setVideoLoading(true);
    setQuizLoading(true);

    const formData = new FormData();
    formData.append('prompt', prompt);
    if (pdfFile) {
      formData.append('pdf', pdfFile);
    }

    // Start video generation
    const videoPromise = fetch(`${API_BASE_URL}/api/generate-video`, {
      method: 'POST',
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        console.log('Video API Response:', data);
        if (data.success && data.final_video_url) {
          setVideoData({
            videoUrl: `${API_BASE_URL}${data.final_video_url}`,
            narrationScript: data.script_text || '',
            videoId: data.video_id || '',
          });

          // Update lesson context
          updateLesson({
            prompt: prompt,
            videoUrl: `${API_BASE_URL}${data.final_video_url}`,
            narrationScript: data.script_text || '',
            videoId: data.video_id || '',
            sharedToCommunity: false,
            loading: false,
          });
        } else {
          setError(data.error || data.video_error || 'Failed to generate video');
        }
      })
      .catch(err => {
        console.error('Video generation error:', err);
        setError('Failed to generate video: ' + err.message);
      })
      .finally(() => {
        setVideoLoading(false);
      });

    // Start quiz generation
    const quizPromise = fetch(`${API_BASE_URL}/api/generate-quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: prompt }),
    })
      .then(res => res.json())
      .then(data => {
        console.log('Quiz API Response:', data);
        if (data.success) {
          setQuizData({ questions: data.questions });
          setQuizId(data.quiz_id);
        } else {
          console.warn('Quiz generation failed:', data.error);
        }
      })
      .catch(err => {
        console.error('Quiz generation error:', err);
      })
      .finally(() => {
        setQuizLoading(false);
      });

    // Wait for both (but they run independently)
    await Promise.allSettled([videoPromise, quizPromise]);
  };

  return (
    <div className="video-generator">
      {/* Input Section */}
      <motion.div 
        className="input-section"
        initial={showSplash ? { opacity: 0, y: 20 } : { opacity: 1, y: 0 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: showSplash ? 0.3 : 0 }}
      >
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
              disabled={videoLoading || quizLoading}
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
                disabled={videoLoading || quizLoading}
                className="attach-btn celestial-btn"
                title="Attach PDF"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                </svg>
              </button>

              <button
                onClick={handleGenerate}
                disabled={(videoLoading || quizLoading) || !prompt.trim()}
                className="send-btn celestial-btn"
                title="Generate Animation"
              >
                {(videoLoading || quizLoading) ? (
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
      </motion.div>

      {/* Error Message */}
      {error && (
        <div className="message-card error-message">
          <div className="message-icon">✕</div>
          <p>{error}</p>
        </div>
      )}

      {/* Video Loading */}
      {videoLoading && (
        <div className="message-card loading-message">
          <ConstellationLoading />
          <p style={{ marginTop: '1rem', color: '#9ca3af' }}>Generating your video...</p>
        </div>
      )}

      {/* Video Section */}
      {videoData && (
        <div className="video-section">
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
            {videoData?.videoId && (
              <div className="share-section">
                {!currentLesson.sharedToCommunity ? (
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
          </div>

          <div className="video-container">
            <video
              ref={videoRef}
              controls
              key={videoData.videoUrl}
              className="video-player"
            >
              <source src={videoData.videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      )}

      {/* Quiz Loading */}
      {quizLoading && (
        <div className="message-card loading-message" style={{ marginTop: '2rem' }}>
          <ConstellationLoading />
          <p style={{ marginTop: '1rem', color: '#9ca3af' }}>Generating your quiz...</p>
        </div>
      )}

      {/* Quiz Section */}
      {quizData && quizId && (
        <div className="quiz-section">
          <QuizContainer quizData={quizData} quizId={quizId} />
        </div>
      )}
    </div>
  );
}

export default VideoGenerator;
