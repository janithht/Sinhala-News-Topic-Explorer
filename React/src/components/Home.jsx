import React, { useState } from 'react';
import './Home.css';

export default function Home({ onSubmit, loading }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text);
    }
  };

  return (
    <section className="home-section">
      <div className="home-card">
        <h2 className="home-title">Sinhala News Article</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            className="home-textarea"
            rows={6}
            placeholder="Paste your Sinhala news article or paragraph here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            className="home-submit-btn"
            disabled={loading || !text.trim()}
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
      </div>
    </section>
  );
}
