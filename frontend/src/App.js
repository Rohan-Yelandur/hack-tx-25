import './App.css';
import { useState } from 'react';

function App() {
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
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();

      if (data.success) {
        setVideoUrl(`http://localhost:5000${data.video_url}`);
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
    <div className="App">
      <header className="App-header">
        <h1>Manim Video Generator</h1>
        <p>Generate educational animations with AI</p>
      </header>

      <main className="App-main">
        <div className="input-section">
          <div className="form-group">
            <label htmlFor="prompt">Prompt:</label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the animation you want to create..."
              rows="4"
              disabled={loading}
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

        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

        {loading && (
          <div className="loading-message">
            <p>🎬 Generating your animation... This may take a minute.</p>
          </div>
        )}

        {videoUrl && (
          <div className="video-section">
            <h2>Generated Video</h2>
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

            {manimCode && (
              <details className="code-section">
                <summary>View Generated Code</summary>
                <pre>{manimCode}</pre>
              </details>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
