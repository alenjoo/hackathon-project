import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <main className="landing-wrapper">
      <header className="landing-header">
        <h1>Welcome to GovTech Portal</h1>
        <p className="tagline">
          Seamlessly manage your service requests and payments — fast, secure, and user-friendly.
        </p>
      </header>

      <section className="cta-section">
        <div className="cta-card">
          <h2>Get Started</h2>
          <p>Access your dashboard, submit requests, and stay updated.</p>
          <div className="cta-buttons">
            <Link to="/login" className="auth-btn">Login</Link>
            <Link to="/signup" className="auth-btn secondary">Sign Up</Link>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <p>&copy; 2025 GovTech Simulation • Built for speed and security</p>
      </footer>
    </main>
  );
};

export default LandingPage;
