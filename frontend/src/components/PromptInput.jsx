import { useState } from 'react';

export default function PromptInput({ onGenerate, loading }) {
  const [topic, setTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic.trim()) return;
    onGenerate(topic);
  };

  return (
    <div className="prompt-input">
      <h2>2. Generate Mock Test</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="e.g. Distillation Column Reflux Ratio" 
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          disabled={loading}
          style={{ width: '300px', padding: '8px' }}
        />
        <button type="submit" disabled={loading || !topic.trim()} style={{ padding: '8px 16px', marginLeft: '8px' }}>
          Generate Test
        </button>
      </form>
    </div>
  );
}
