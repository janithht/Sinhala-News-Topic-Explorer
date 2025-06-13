import React, { useState } from 'react';
import Header from './components/Header';
import Home from './components/Home';
import './App.css';
import axios from 'axios';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (text) => {
    setLoading(true);
    setResults(null);
    setError(null);
    try {
      const resp = await axios.post('/api/infer_topic', { text });
      setResults(resp.data);
    } catch (err) {
      setError('Failed to fetch topics');
    } finally {
      setLoading(false);
    }
  };

  const topTopic =
    results && results.length
      ? results.reduce((max, item) => (item.score > max.score ? item : max), results[0])
      : null;

  return (
    <div className="app-bg">
      <Header />
      <Home onSubmit={handleAnalyze} loading={loading} />

      <div className="response-container">
        {error && <p className="error-message">{error}</p>}

        {topTopic && (
          <div className="results">
            <h2>Top Topic</h2>
            <div className="topic-card">
              <h3>
                {topTopic.label}{' '}
                <span style={{ color: '#888', fontWeight: 400 }}>
                  ({(topTopic.score * 100).toFixed(1)}%)
                </span>
              </h3>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
