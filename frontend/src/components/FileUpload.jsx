import { useState } from 'react';

export default function FileUpload({ onUploadSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    if (file.type !== 'application/pdf') {
      setError('Only PDF files are allowed.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be under 5MB.');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const { uploadFile } = await import('../api');
      const data = await uploadFile(file);
      onUploadSuccess(data.doc_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading file. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload">
      <h2>1. Upload Syllabus (PDF)</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} disabled={loading} />
      {loading && <p>Parsing document... please wait.</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}
