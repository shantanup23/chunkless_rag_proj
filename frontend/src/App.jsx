import { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import PromptInput from './components/PromptInput';
import TestViewer from './components/TestViewer';
import { generateTest } from './api';
import './App.css';

function App() {
  const [docId, setDocId] = useState(sessionStorage.getItem('active_doc_id') || null);
  const [testData, setTestData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (docId) {
      sessionStorage.setItem('active_doc_id', docId);
    }
  }, [docId]);

  const handleUploadSuccess = (newDocId) => {
    setDocId(newDocId);
    setTestData(null);
    setError('');
  };

  const handleGenerate = async (topic) => {
    setLoading(true);
    setError('');
    try {
      const payload = {
        doc_id: docId,
        topic_prompt: topic,
        chat_history: []
      };
      const data = await generateTest(payload);
      setTestData(data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to generate test. Ensure backend is running and doc is valid.';
      setError(errorMsg);
      if (errorMsg.includes('DOCUMENT_NOT_FOUND')) {
        setDocId(null);
        sessionStorage.removeItem('active_doc_id');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chunkless RAG Mock Test Generator</h1>
      </header>
      <main>
        {!docId ? (
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        ) : (
          <div>
            <div className="success-banner">Document uploaded successfully! (Session Active)</div>
            <PromptInput onGenerate={handleGenerate} loading={loading} />
            {loading && <p style={{ color: '#0066cc', fontWeight: 'bold' }}>Generating your test... this may take 10-30 seconds.</p>}
            {error && <p className="error">{error}</p>}
            <TestViewer testData={testData} />
            <button onClick={() => { setDocId(null); sessionStorage.removeItem('active_doc_id'); }} style={{ marginTop: '20px', padding: '8px 16px', background: '#eee', border: '1px solid #ccc', cursor: 'pointer' }}>Upload a Different Syllabus</button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
