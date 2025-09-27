import React, { useState, useRef } from 'react';
import './App.css';

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0] && files[0].type.includes('video')) {
      setSelectedFile(files[0]);
      setResult(null);
      console.log('File selected via drag & drop:', files[0].name);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type.includes('video')) {
      setSelectedFile(file);
      setResult(null);
      console.log('File selected via input:', file.name);
    } else {
      console.log('No valid video file selected');
    }
  };

  const simulateProgress = () => {
    setAnalysisProgress(0);
    const interval = setInterval(() => {
      setAnalysisProgress(prev => {
        if (prev >= 90) {
          clearInterval(interval);
          return 90;
        }
        return prev + Math.random() * 15;
      });
    }, 500);
    return interval;
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      console.log('No file selected');
      return;
    }

    console.log('Starting analysis for file:', selectedFile.name);
    setIsAnalyzing(true);
    setResult(null);
    const progressInterval = simulateProgress();

    try {
      const formData = new FormData();
      formData.append('video', selectedFile);

      console.log('Sending request to backend...');
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log('Analysis result:', data);
      
      setAnalysisProgress(100);
      setTimeout(() => {
        setResult(data);
      }, 500);
      
    } catch (error) {
      console.error('Error analyzing video:', error);
      setResult({
        status: 'error',
        message: 'Failed to analyze video. Please make sure the backend server is running on port 5000.'
      });
    } finally {
      clearInterval(progressInterval);
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    console.log('Resetting application...');
    setSelectedFile(null);
    setResult(null);
    setAnalysisProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const debugState = () => {
    console.log('Current State:', {
      selectedFile: selectedFile?.name || 'null',
      isAnalyzing,
      hasResult: !!result,
      progress: analysisProgress
    });
  };

  const getResultDescription = (result) => {
    if (!result || result.status === 'error') return '';
    
    if (result.label && result.label.includes('FAKE')) {
      return "This video shows signs of AI manipulation. Exercise caution when sharing or believing its content.";
    } else if (result.label && result.label.includes('REAL')) {
      return "This video appears to be authentic. No significant signs of AI manipulation detected.";
    }
    return "Analysis complete. Review the results above.";
  };

  return (
    <div className="app">
      <div className="background-animation">
        <div className="floating-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
        </div>
      </div>

      <div className="container">
        <header className="header">
          <div className="logo">
            {/* <div className="logo-icon">
              <div className="logo-eye"></div>
              <div className="logo-sparkle"></div>
            </div> */}
            <img src={"/logo.png"} alt="ReaLies Logo" className="logo-icon" />
            <h1>ReaLies</h1>
          </div>
          <p className="tagline">AI-Powered Video Authenticity Analysis</p>
          
        </header>

        <main className="main-content">
          <section className="upload-section">
            <div className="upload-card">
              <div className="card-glow"></div>
              
              <div className="card-header">
                <h2>Upload Video for Analysis</h2>
                <p>Detect AI-generated content with advanced deep learning algorithms</p>
              </div>

              <div 
                className={`upload-area ${dragActive ? 'drag-active' : ''} ${selectedFile ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => {
                  console.log('Upload area clicked');
                  fileInputRef.current?.click();
                }}
                style={{ cursor: 'pointer' }}
              >
                <div className="upload-content">
                  <div className="upload-icon">
                    <div className="cloud-icon"></div>
                    <div className="video-icon"></div>
                  </div>
                  
                  {!selectedFile ? (
                    <>
                      <h3>Drop your video here</h3>
                      <p>or click to browse files</p>
                      <p className="file-types">Supported: MP4, AVI, MOV, WMV</p>
                    </>
                  ) : (
                    <>
                      <h3>Video Selected</h3>
                      <p className="file-name">{selectedFile.name}</p>
                      <p className="file-size">
                        {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                      </p>
                    </>
                  )}
                  
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="video/*"
                    onChange={handleFileSelect}
                    className="file-input"
                  />
                </div>
              </div>

              {isAnalyzing && (
                <div className="progress-section">
                  <div className="progress-header">
                    <span>Analyzing Video</span>
                    <span>{Math.round(analysisProgress)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill"
                      style={{ width: `${analysisProgress}%` }}
                    ></div>
                  </div>
                  <div className="progress-steps">
                    <span className={analysisProgress > 0 ? 'active' : ''}>Uploading</span>
                    <span className={analysisProgress > 25 ? 'active' : ''}>Processing</span>
                    <span className={analysisProgress > 50 ? 'active' : ''}>Analyzing</span>
                    <span className={analysisProgress > 75 ? 'active' : ''}>Finalizing</span>
                  </div>
                </div>
              )}

              <div className="action-buttons">
                <button 
                  className={`btn secondary ${!selectedFile && !result ? 'disabled' : ''}`}
                  onClick={handleReset}
                  disabled={isAnalyzing}
                >
                  <span className="btn-icon">↺</span>
                  Reset
                </button>
                <button 
                  className={`btn primary ${isAnalyzing ? 'analyzing' : ''} ${!selectedFile ? 'disabled' : ''}`}
                  onClick={handleAnalyze}

                >
                  {isAnalyzing ? (
                    <>
                      <div className="spinner"></div>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <span className="btn-icon">🔍</span>
                      Analyze Video
                    </>
                  )}
                </button>
              </div>

              <div className="status-info">
                {!selectedFile && (
                  <p className="status-message">Please select a video file to begin analysis</p>
                )}
                {selectedFile && !isAnalyzing && !result && (
                  <p className="status-message ready">Video selected and ready for analysis</p>
                )}
              </div>
            </div>
          </section>

          {result && (
            <section className="results-section">
              <div className={`result-card ${result.status === 'error' ? 'error' : result.label?.includes('FAKE') ? 'fake' : 'real'}`}>
                <div className="result-glow"></div>
                
                <div className="result-header">
                  <h2>Analysis Results</h2>
                  <div className="result-icon">
                    {result.status === 'error' ? '❌' : result.label?.includes('FAKE') ? '⚠️' : '✅'}
                  </div>
                </div>
                
                {result.status === 'error' ? (
                  <div className="result-content">
                    <p className="error-message">{result.message}</p>
                  </div>
                ) : (
                  <div className="result-content">
                    <div className="result-badge">
                      <span className={`label ${result.label?.includes('FAKE') ? 'fake' : 'real'}`}>
                        {result.label || 'Unknown'}
                      </span>
                      {result.probability && (
                        <span className="confidence">
                          Confidence: {(result.probability * 100).toFixed(1)}%
                        </span>
                      )}
                    </div>
                    
                    <div className="result-description">
                      <p>{getResultDescription(result)}</p>
                    </div>

                    {result.probability && (
                      <div className="confidence-meter">
                        <div className="meter-labels">
                          <span>Real</span>
                          <span>Fake</span>
                        </div>
                        <div className="meter-track">
                          <div 
                            className="meter-fill"
                            style={{ 
                              width: `${result.probability * 100}%`,
                              background: result.label?.includes('FAKE') 
                                ? 'linear-gradient(90deg, #ff6b6b, #ff8e8e)'
                                : 'linear-gradient(90deg, #51cf66, #94d82d)'
                            }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                <div className="result-actions">
                  <button className="btn secondary" onClick={handleReset}>
                    <span className="btn-icon">📁</span>
                    Analyze Another Video
                  </button>
                </div>
              </div>
            </section>
          )}
          <section className="info-section">
            <div className="info-cards">
              <div className="info-card">
                <div className="info-icon">🤖</div>
                <h3>AI Technology</h3>
                <p>Uses advanced CNN-RNN models trained on thousands of real and fake videos</p>
              </div>
              
              <div className="info-card">
                <div className="info-icon">⚡</div>
                <h3>Fast Analysis</h3>
                <p>Get results in seconds with our optimized deep learning pipeline</p>
              </div>
              
              <div className="info-card">
                <div className="info-icon">🔒</div>
                <h3>Privacy First</h3>
                <p>Your videos are processed locally and never stored on our servers</p>
              </div>
            </div>
          </section>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>ReaLies v1.0 • Virly | Kevin | Darwin</p>
        </footer>
      </div>
    </div>
  );
};

export default App;