import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, Code, Brain, Users, Shield, MessageSquare, ArrowRight, Star } from 'lucide-react';
import './Landing.css';

const Landing = () => {
  const features = [
    { icon: Code, title: 'Coding Space', description: 'Build, test, and share your code projects with our integrated development environment.' },
    { icon: Brain, title: 'Mind Space', description: 'AI-powered mental health support and personalized wellness recommendations.' },
    { icon: Users, title: 'Community Support', description: 'Connect with peers and join group discussions for mutual support and growth.' },
    { icon: Shield, title: 'Safe Environment', description: 'Secure and confidential platform designed with your privacy and safety in mind.' },
    { icon: MessageSquare, title: 'AI Assistant', description: 'Get instant help and guidance from our intelligent AI assistant, Coby.' },
    { icon: Star, title: 'Personal Growth', description: 'Track your progress and achieve your goals with personalized insights and analytics.' }
  ];

  const testimonials = [
    { name: 'Sarah Johnson', role: 'Software Developer', content: 'Coby has been a game-changer for my mental health journey. The AI support is incredibly helpful.', rating: 5 },
    { name: 'Michael Chen', role: 'Student', content: 'The coding space feature helped me learn programming while maintaining my mental wellness.', rating: 5 },
    { name: 'Emily Rodriguez', role: 'Designer', content: "I love the community aspect. It's great to connect with others who understand the challenges.", rating: 5 }
  ];

  return (
    <div className="landing">
      {/* Header */}
      <header className="landing-header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <Bot className="logo-icon" />
              <span className="logo-text">Coby</span>
            </div>
            <nav className="nav-menu">
              <Link to="/features">Features</Link>
              <Link to="/about">About</Link>
              <Link to="/testimonials">Testimonials</Link>
              <Link to="/contact">Contact</Link>
            </nav>
            <div className="header-actions">
              <Link to="/login" className="login-btn">Sign In</Link>
              <Link to="/signup" className="signup-btn">Get Started</Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <div className="hero-text">
              <h1>Your AI-Powered Companion for Growth & Wellness</h1>
              <p>
                Coby combines cutting-edge AI technology with mental health support,
                coding tools, and community features to help you thrive in both your
                personal and professional journey.
              </p>
              <div className="hero-actions">
                <Link to="/signup" className="cta-primary">
                  Start Your Journey
                  <ArrowRight className="icon" />
                </Link>
                <Link to="/login" className="cta-secondary">Sign In</Link>
              </div>
              <div className="hero-stats">
                <div className="stat">
                  <span className="stat-number">10K+</span>
                  <span className="stat-label">Active Users</span>
                </div>
                <div className="stat">
                  <span className="stat-number">95%</span>
                  <span className="stat-label">Satisfaction Rate</span>
                </div>
                <div className="stat">
                  <span className="stat-number">24/7</span>
                  <span className="stat-label">AI Support</span>
                </div>
              </div>
            </div>
            <div className="hero-visual">
              <div className="hero-card">
                <Bot className="hero-icon" />
                <h3>Meet Coby</h3>
                <p>Your intelligent AI assistant ready to help you grow</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features">
        <div className="container">
          <div className="section-header">
            <h2>Features</h2>
            <p>Explore what Coby offers to help you grow and thrive.</p>
          </div>
          <div className="features-grid">
            {features.map((feature, idx) => (
              <div className="feature-card" key={idx}>
                <feature.icon className="feature-icon" />
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section - New Design */}
      <section id="testimonials" className="testimonials new-landing-section">
        <div className="container">
          <div className="section-header">
            <h2>What Our Users Say</h2>
            <p>Discover a new way to grow, learn, and thrive with Coby.</p>
          </div>


          {/* Optional: list-style testimonials */}
          <div className="testimonials-list">
            {testimonials.map((t, idx) => (
              <div className="testimonial-card" key={idx}>
                <div className="testimonial-rating">
                  {[...Array(t.rating)].map((_, i) => (
                    <Star key={i} size={18} color="#fbbf24" fill="#fbbf24" />
                  ))}
                </div>
                <div className="testimonial-content">"{t.content}"</div>
                <div className="testimonial-user">
                  <span className="testimonial-name">{t.name}</span> - <span className="testimonial-role">{t.role}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h4>Product</h4>
              <Link to="/features">Features</Link>
              <Link to="/about">About</Link>
              <Link to="/testimonials">Testimonials</Link>
              <Link to="/contact">Contact</Link>
              <Link to="/community">Community</Link>
            </div>
            <div className="footer-section">
              <h4>Support</h4>
              <Link to="/help">Help Center</Link>
              <Link to="/contact">Contact</Link>
              <Link to="/community">Community</Link>
            </div>
            <div className="footer-section">
              <h4>Legal</h4>
              <Link to="/privacy">Privacy</Link>
              <Link to="/terms">Terms</Link>
              <Link to="/security">Security</Link>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Coby. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;