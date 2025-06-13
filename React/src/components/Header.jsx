import React from 'react';
import './Header.css';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-content">
        <span className="header-icon" role="img" aria-label="Globe">🌐</span>
        <div>
          <h1>Sinhala News Topic Explorer</h1>
          <p className="header-subtitle">
            Discover topics in your Sinhala news instantly!
          </p>
        </div>
      </div>
    </header>
  );
}
