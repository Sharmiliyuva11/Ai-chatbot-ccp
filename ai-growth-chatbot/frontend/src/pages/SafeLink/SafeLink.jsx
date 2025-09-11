import React, { useState } from 'react';
import {
  Shield,
  Phone,
  MessageCircle,
  MapPin,
  Clock,
  Heart,
  AlertTriangle,
  ExternalLink,
  Search,
  Filter
} from 'lucide-react';
import api from '../../services/api';
import './SafeLink.css';

const SafeLink = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [localSearchTerm, setLocalSearchTerm] = useState('');
  const [localResults, setLocalResults] = useState([]);
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState('');

  const emergencyContacts = [
    {
      id: 1,
      name: 'National Suicide Prevention Lifeline',
      number: '988',
      description: '24/7 free and confidential support for people in distress',
      category: 'crisis',
      available: '24/7',
      languages: ['English', 'Spanish'],
      type: 'phone'
    },
    {
      id: 2,
      name: 'Crisis Text Line',
      number: 'Text HOME to 741741',
      description: 'Free, 24/7 support for those in crisis',
      category: 'crisis',
      available: '24/7',
      languages: ['English'],
      type: 'text'
    },
    {
      id: 3,
      name: 'SAMHSA National Helpline',
      number: '1-800-662-4357',
      description: 'Treatment referral and information service',
      category: 'substance',
      available: '24/7',
      languages: ['English', 'Spanish'],
      type: 'phone'
    },
    {
      id: 4,
      name: 'National Domestic Violence Hotline',
      number: '1-800-799-7233',
      description: 'Support for domestic violence survivors',
      category: 'domestic',
      available: '24/7',
      languages: ['English', 'Spanish', '200+ languages'],
      type: 'phone'
    }
  ];

  const resources = [
    {
      id: 1,
      title: 'Mental Health America',
      description: 'Comprehensive mental health resources and screening tools',
      url: 'https://mhanational.org',
      category: 'mental-health',
      type: 'website'
    },
    {
      id: 2,
      title: 'NAMI (National Alliance on Mental Illness)',
      description: 'Support groups, education, and advocacy',
      url: 'https://nami.org',
      category: 'mental-health',
      type: 'website'
    },
    {
      id: 3,
      title: 'Psychology Today Therapist Finder',
      description: 'Find mental health professionals in your area',
      url: 'https://psychologytoday.com',
      category: 'therapy',
      type: 'website'
    },
    {
      id: 4,
      title: 'BetterHelp',
      description: 'Online counseling and therapy services',
      url: 'https://betterhelp.com',
      category: 'therapy',
      type: 'website'
    }
  ];

  const categories = [
    { id: 'all', name: 'All Resources', icon: Shield },
    { id: 'crisis', name: 'Crisis Support', icon: AlertTriangle },
    { id: 'mental-health', name: 'Mental Health', icon: Heart },
    { id: 'therapy', name: 'Therapy', icon: MessageCircle },
    { id: 'substance', name: 'Substance Abuse', icon: Shield },
    { id: 'domestic', name: 'Domestic Violence', icon: Shield }
  ];

  const filteredContacts = emergencyContacts.filter(contact => 
    (selectedCategory === 'all' || contact.category === selectedCategory) &&
    (contact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
     contact.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const filteredResources = resources.filter(resource => 
    (selectedCategory === 'all' || resource.category === selectedCategory) &&
    (resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
     resource.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleCall = (number) => {
    window.open(`tel:${number}`, '_self');
  };

  const handleText = (number) => {
    window.open(`sms:${number}`, '_self');
  };

  const handleLocalSearch = async () => {
    if (!localSearchTerm.trim()) {
      setLocalError('Please enter a zip code or city name.');
      setLocalResults([]);
      return;
    }
    setLocalLoading(true);
    setLocalError('');
    setLocalResults([]);
    try {
      // Call the backend API to search for local mental health support services
      const response = await api.searchLocalSupport(localSearchTerm.trim(), 'all');

      if (response.success && response.results) {
        setLocalResults(response.results);
        if (response.results.length === 0) {
          setLocalError('No local support found for the given location.');
        }
      } else {
        setLocalError(response.error || 'Failed to search local support. Please try again.');
      }
    } catch (err) {
      console.error('Local search error:', err);
      setLocalError('Failed to search local support. Please try again.');
    } finally {
      setLocalLoading(false);
    }
  };

  return (
    <div className="safe-link">
      <div className="safe-link-header">
        <div className="header-content">
          <h1>Safe Link</h1>
          <p>Emergency contacts, crisis support, and mental health resources</p>
        </div>
        <div className="emergency-banner">
          <AlertTriangle className="warning-icon" />
          <div>
            <span className="emergency-text">In immediate danger?</span>
            <button className="emergency-btn" onClick={() => handleCall('911')}>
              Call 911 Now
            </button>
          </div>
        </div>
      </div>

      <div className="search-filter-section">
        <div className="search-container">
          <Search className="search-icon" />
          <input
            type="text"
            placeholder="Search resources..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="filter-container">
          <Filter className="filter-icon" />
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="categories-grid">
        {categories.map(category => (
          <button
            key={category.id}
            className={`category-card ${selectedCategory === category.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(category.id)}
          >
            <category.icon className="category-icon" />
            <span>{category.name}</span>
          </button>
        ))}
      </div>

      <div className="content-sections">
        <section className="emergency-contacts">
          <h2>Emergency Contacts & Crisis Support</h2>
          <div className="contacts-grid">
            {filteredContacts.map(contact => (
              <div key={contact.id} className="contact-card">
                <div className="contact-header">
                  <div className="contact-info">
                    <h3>{contact.name}</h3>
                    <p>{contact.description}</p>
                  </div>
                  <div className="contact-type">
                    {contact.type === 'phone' ? (
                      <Phone className="type-icon" />
                    ) : (
                      <MessageCircle className="type-icon" />
                    )}
                  </div>
                </div>

                <div className="contact-details">
                  <div className="detail-item">
                    <Clock className="detail-icon" />
                    <span>Available: {contact.available}</span>
                  </div>
                  <div className="detail-item">
                    <MessageCircle className="detail-icon" />
                    <span>Languages: {contact.languages.join(', ')}</span>
                  </div>
                </div>

                <div className="contact-number">
                  <span className="number">{contact.number}</span>
                </div>

                <div className="contact-actions">
                  {contact.type === 'phone' ? (
                    <button 
                      className="action-btn primary"
                      onClick={() => handleCall(contact.number)}
                    >
                      <Phone className="btn-icon" />
                      Call Now
                    </button>
                  ) : (
                    <button 
                      className="action-btn primary"
                      onClick={() => handleText(contact.number.split(' ').pop())}
                    >
                      <MessageCircle className="btn-icon" />
                      Text Now
                    </button>
                  )}
                  <button className="action-btn secondary">
                    <Heart className="btn-icon" />
                    Save
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="resources-section">
          <h2>Mental Health Resources</h2>
          <div className="resources-grid">
            {filteredResources.map(resource => (
              <div key={resource.id} className="resource-card">
                <div className="resource-content">
                  <h3>{resource.title}</h3>
                  <p>{resource.description}</p>
                </div>
                <div className="resource-actions">
                  <button 
                    className="resource-btn"
                    onClick={() => window.open(resource.url, '_blank')}
                  >
                    <ExternalLink className="btn-icon" />
                    Visit Website
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="local-resources">
          <h2>Find Local Support</h2>
          <div className="local-finder">
            <div className="finder-content">
              <MapPin className="finder-icon" />
              <div>
                <h3>Local Mental Health Services</h3>
                <p>Find therapists, support groups, and mental health facilities near you</p>
              </div>
            </div>
            <div className="location-input">
              <input 
                type="text" 
                placeholder="Enter your zip code or city" 
                value={localSearchTerm}
                onChange={(e) => setLocalSearchTerm(e.target.value)}
              />
              <button className="search-btn" onClick={handleLocalSearch}>
                <Search className="btn-icon" />
                Search
              </button>
            </div>
          </div>
          {localLoading && <p>Loading local support...</p>}
          {localError && <p className="error-message">{localError}</p>}
          {localResults.length > 0 && (
            <div className="local-results">
              <h3>Local Support Results</h3>
              <ul>
                {localResults.map((item, index) => (
                  <li key={index}>
                    <strong>{item.name || item.title}</strong>: {item.description}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>

        <section className="safety-tips">
          <h2>Safety & Wellness Tips</h2>
          <div className="tips-grid">
            <div className="tip-card">
              <Shield className="tip-icon" />
              <h4>Create a Safety Plan</h4>
              <p>Develop a personalized plan for managing crisis situations and staying safe.</p>
            </div>
            <div className="tip-card">
              <Heart className="tip-icon" />
              <h4>Build Your Support Network</h4>
              <p>Identify trusted friends, family members, and professionals you can reach out to.</p>
            </div>
            <div className="tip-card">
              <Phone className="tip-icon" />
              <h4>Keep Important Numbers Handy</h4>
              <p>Save crisis hotlines and emergency contacts in your phone for quick access.</p>
            </div>
            <div className="tip-card">
              <MessageCircle className="tip-icon" />
              <h4>Know the Warning Signs</h4>
              <p>Learn to recognize when you or someone else might need immediate help.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default SafeLink;
