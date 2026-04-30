import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      processImage(file);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      processImage(file);
    }
  };

  const processImage = (file) => {
    // Reset states
    setResult(null);
    setError(null);
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (JPEG, PNG, etc.)');
      return;
    }
    
    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size should be less than 10MB');
      return;
    }
    
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data.result);
    } catch (err) {
      if (err.response) {
        setError(err.response.data.detail || 'Server error occurred');
      } else if (err.request) {
        setError('Cannot connect to server. Make sure the backend is running.');
      } else {
        setError('An error occurred while processing the image');
      }
    } finally {
      setLoading(false);
    }
  };

  const resetAll = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🧠 Brain Tumor Detection</h1>
        <p className="subtitle">Upload an MRI scan for AI-powered analysis</p>
      </header>

      <main className="main-content">
        <div className="upload-section">
          {!previewUrl ? (
            <div
              className={`upload-area ${dragActive ? 'drag-active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => document.getElementById('fileInput').click()}
            >
              <div className="upload-content">
                <span className="upload-icon">📁</span>
                <h3>Drag & Drop your MRI image here</h3>
                <p>or click to browse</p>
                <p className="upload-hint">Supports: JPEG, PNG (Max 10MB)</p>
              </div>
              <input
                id="fileInput"
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
              />
            </div>
          ) : (
            <div className="preview-section">
              <h3>Selected Image:</h3>
              <div className="image-preview">
                <img src={previewUrl} alt="Selected MRI" />
              </div>
              <div className="button-group">
                <button 
                  onClick={handlePredict} 
                  disabled={loading}
                  className="predict-btn"
                >
                  {loading ? '🔍 Analyzing...' : '🔍 Predict'}
                </button>
                <button onClick={resetAll} className="reset-btn">
                  🔄 Upload New Image
                </button>
              </div>
            </div>
          )}
        </div>

        {loading && (
          <div className="loading-section">
            <div className="spinner"></div>
            <p>Analyzing MRI image...</p>
          </div>
        )}

        {error && (
          <div className="error-section">
            <span className="error-icon">⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className={`result-section ${result.prediction === 'Tumor Detected' ? 'tumor' : 'no-tumor'}`}>
            <h2>Analysis Results</h2>
            <div className="result-card">
              <div className="prediction-badge">
                <span className="prediction-label">Prediction:</span>
                <span className={`prediction-value ${result.prediction === 'Tumor Detected' ? 'tumor-text' : 'no-tumor-text'}`}>
                  {result.prediction}
                </span>
              </div>

              <div className="confidence-section">
                <div className="confidence-bar-container">
                  <div 
                    className="confidence-bar" 
                    style={{ width: `${result.confidence}%` }}
                  ></div>
                </div>
                <div className="confidence-details">
                  <span>Confidence: {result.confidence}%</span>
                  <span className="confidence-level">({result.confidence_level})</span>
                </div>
              </div>

              <div className="reasoning-section">
                <h4>📋 Analysis Reasoning:</h4>
                <p>{result.reasoning}</p>
              </div>

              <div className="disclaimer">
                <p>⚠️ <strong>Disclaimer:</strong> This is an AI-assisted tool and should not be used as the sole basis for medical decisions. Always consult with a qualified healthcare professional.</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;