import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, Code, Brain, Users, Shield, MessageSquare, ArrowRight, Star, CheckCircle } from 'lucide-react';
import './Landing.css';

const Landing = () => {
  const features = [
    {
      icon: Code,
      title: 'Coding Space',
      description: 'Build, test, and share your code projects with our integrated development environment.'
    },
    {
      icon: Brain,
      title: 'Mind Space',
      description: 'AI-powered mental health support and personalized wellness recommendations.'
    },
    {
      icon: Users,
      title: 'Community Support',
      description: 'Connect with peers and join group discussions for mutual support and growth.'
    },
    {
      icon: Shield,
      title: 'Safe Environment',
      description: 'Secure and confidential platform designed with your privacy and safety in mind.'
    },
    {
      icon: MessageSquare,
      title: 'AI Assistant',
      description: 'Get instant help and guidance from our intelligent AI assistant, Cally.'
    },
    {
      icon: Star,
      title: 'Personal Growth',
      description: 'Track your progress and achieve your goals with personalized insights and analytics.'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Software Developer',
      content: 'Cally has been a game-changer for my mental health journey. The AI support is incredibly helpful.',
      rating: 5
    },
    {
      name: 'Michael Chen',
      role: 'Student',
      content: 'The coding space feature helped me learn programming while maintaining my mental wellness.',
      rating: 5
    },
    {
      name: 'Emily Rodriguez',
      role: 'Designer',
      content: 'I love the community aspect. It\'s great to connect with others who understand the challenges.',
      rating: 5
    }
  ];

  return (
    <div className="landing">
      {/* Header */}
      <header className="landing-header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <Bot className="logo-icon" />
              <span className="logo-text">Cally</span>
            </div>
            <nav className="nav-menu">
              <a href="#features">Features</a>
              <a href="#about">About</a>
              <a href="#testimonials">Testimonials</a>
              <a href="#contact">Contact</a>
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
                Cally combines cutting-edge AI technology with mental health support, 
                coding tools, and community features to help you thrive in both your 
                personal and professional journey.
              </p>
              <div className="hero-actions">
                <Link to="/signup" className="cta-primary">
                  Start Your Journey
                  <ArrowRight className="icon" />
                </Link>
                <Link to="/login" className="cta-secondary">
                  Sign In
                </Link>
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
                <h3>Meet Cally</h3>
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
            <h2>Everything You Need to Thrive</h2>
            <p>Discover the powerful features that make Cally your perfect companion</p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">
                  <feature.icon />
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about">
        <div className="container">
          <div className="about-content">
            <div className="about-text">
              <h2>Why Choose Cally?</h2>
              <p>
                Cally is more than just an AI assistant. We're your comprehensive platform 
                for personal and professional growth, combining mental health support with 
                practical tools for learning and development.
              </p>
              <div className="about-features">
                <div className="about-feature">
                  <CheckCircle className="check-icon" />
                  <span>AI-powered personalized support</span>
                </div>
                <div className="about-feature">
                  <CheckCircle className="check-icon" />
                  <span>Secure and confidential environment</span>
                </div>
                <div className="about-feature">
                  <CheckCircle className="check-icon" />
                  <span>Integrated coding and learning tools</span>
                </div>
                <div className="about-feature">
                  <CheckCircle className="check-icon" />
                  <span>Supportive community network</span>
                </div>
              </div>
            </div>
            <div className="about-visual">
              <div className="about-stats">
                <div className="about-stat">
                  <h3>99.9%</h3>
                  <p>Uptime</p>
                </div>
                <div className="about-stat">
                  <h3>50+</h3>
                  <p>Countries</p>
                </div>
                <div className="about-stat">
                  <h3>24/7</h3>
                  <p>Support</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="testimonials">
        <div className="container">
          <div className="section-header">
            <h2>What Our Users Say</h2>
            <p>Join thousands of satisfied users who have transformed their lives with Cally</p>
          </div>
          <div className="testimonials-grid">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="testimonial-card">
                <div className="testimonial-rating">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="star filled" />
                  ))}
                </div>
                <p>"{testimonial.content}"</p>
                <div className="testimonial-author">
                  <strong>{testimonial.name}</strong>
                  <span>{testimonial.role}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Start Your Journey?</h2>
            <p>Join Cally today and discover a new way to grow, learn, and thrive.</p>
            <div className="cta-actions">
              <Link to="/signup" className="cta-primary">
                Get Started Free
                <ArrowRight className="icon" />
              </Link>
              <p className="cta-note">No credit card required • Free forever plan available</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="logo">
                <Bot className="logo-icon" />
                <span className="logo-text">Cally</span>
              </div>
              <p>Your AI-powered companion for growth and wellness.</p>
            </div>
            <div className="footer-links">
              <div className="footer-section">
                <h4>Product</h4>
                <a href="#features">Features</a>
                <a href="#pricing">Pricing</a>
                <a href="#updates">Updates</a>
              </div>
              <div className="footer-section">
                <h4>Support</h4>
                <a href="#help">Help Center</a>
                <a href="#contact">Contact</a>
                <a href="#community">Community</a>
              </div>
              <div className="footer-section">
                <h4>Legal</h4>
                <a href="#privacy">Privacy</a>
                <a href="#terms">Terms</a>
                <a href="#security">Security</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Cally. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;