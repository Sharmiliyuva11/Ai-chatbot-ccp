import React, { useState } from 'react';
import { 
  User, 
  Mail, 
  Phone, 
  Calendar, 
  MapPin, 
  Edit3, 
  Camera,
  Save,
  X,
  Award,
  Target,
  TrendingUp,
  Heart
} from 'lucide-react';
import './Profile.css';

const Profile = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    dateOfBirth: '1990-05-15',
    location: 'New York, NY',
    bio: 'Mental health advocate and wellness enthusiast. Passionate about helping others on their journey to better mental health.',
    emergencyContact: {
      name: 'Jane Doe',
      relationship: 'Sister',
      phone: '+1 (555) 987-6543'
    }
  });

  const [editData, setEditData] = useState({ ...profileData });

  const stats = [
    {
      icon: Calendar,
      label: 'Days Active',
      value: '45',
      color: 'blue'
    },
    {
      icon: Target,
      label: 'Goals Completed',
      value: '12',
      color: 'green'
    },
    {
      icon: TrendingUp,
      label: 'Mood Streak',
      value: '7 days',
      color: 'purple'
    },
    {
      icon: Heart,
      label: 'Sessions',
      value: '28',
      color: 'red'
    }
  ];

  const achievements = [
    {
      id: 1,
      title: 'First Steps',
      description: 'Completed your first wellness session',
      icon: '🎯',
      earned: true,
      date: '2024-01-15'
    },
    {
      id: 2,
      title: 'Consistent Tracker',
      description: 'Logged mood for 7 consecutive days',
      icon: '📊',
      earned: true,
      date: '2024-01-22'
    },
    {
      id: 3,
      title: 'Community Helper',
      description: 'Participated in 5 group sessions',
      icon: '🤝',
      earned: false,
      progress: 3
    },
    {
      id: 4,
      title: 'Mindfulness Master',
      description: 'Completed 20 meditation sessions',
      icon: '🧘',
      earned: false,
      progress: 15
    }
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'meditation',
      title: 'Morning Mindfulness',
      date: '2024-01-25',
      duration: '10 min'
    },
    {
      id: 2,
      type: 'mood',
      title: 'Mood Check-in',
      date: '2024-01-25',
      value: 'Good (8/10)'
    },
    {
      id: 3,
      type: 'session',
      title: 'Anxiety Support Group',
      date: '2024-01-24',
      duration: '60 min'
    },
    {
      id: 4,
      type: 'goal',
      title: 'Daily Exercise Goal',
      date: '2024-01-24',
      status: 'completed'
    }
  ];

  const handleEdit = () => {
    setIsEditing(true);
    setEditData({ ...profileData });
  };

  const handleSave = () => {
    setProfileData({ ...editData });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditData({ ...profileData });
    setIsEditing(false);
  };

  const handleInputChange = (field, value) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setEditData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }));
    } else {
      setEditData(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const getActivityIcon = (type) => {
    switch (type) {
      case 'meditation': return '🧘';
      case 'mood': return '😊';
      case 'session': return '👥';
      case 'goal': return '🎯';
      default: return '📝';
    }
  };

  return (
    <div className="profile">
      <div className="profile-header">
        <div className="profile-banner">
          <div className="profile-avatar-section">
            <div className="profile-avatar">
              <img 
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face" 
                alt="Profile"
              />
              <button className="avatar-edit-btn">
                <Camera className="icon" />
              </button>
            </div>
            <div className="profile-basic-info">
              <h1>{profileData.name}</h1>
              <p className="profile-bio">{profileData.bio}</p>
              <div className="profile-meta">
                <span><MapPin className="meta-icon" /> {profileData.location}</span>
                <span><Calendar className="meta-icon" /> Member since Jan 2024</span>
              </div>
            </div>
          </div>
          <div className="profile-actions">
            {!isEditing ? (
              <button className="edit-btn" onClick={handleEdit}>
                <Edit3 className="icon" />
                Edit Profile
              </button>
            ) : (
              <div className="edit-actions">
                <button className="save-btn" onClick={handleSave}>
                  <Save className="icon" />
                  Save
                </button>
                <button className="cancel-btn" onClick={handleCancel}>
                  <X className="icon" />
                  Cancel
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="profile-content">
        <div className="profile-main">
          <div className="profile-stats">
            <h2>Your Progress</h2>
            <div className="stats-grid">
              {stats.map((stat, index) => (
                <div key={index} className={`stat-card ${stat.color}`}>
                  <stat.icon className="stat-icon" />
                  <div className="stat-content">
                    <span className="stat-value">{stat.value}</span>
                    <span className="stat-label">{stat.label}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="profile-details">
            <h2>Personal Information</h2>
            <div className="details-form">
              <div className="form-group">
                <label>Full Name</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <User className="field-icon" />
                    <span>{profileData.name}</span>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Email Address</label>
                {isEditing ? (
                  <input
                    type="email"
                    value={editData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <Mail className="field-icon" />
                    <span>{profileData.email}</span>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Phone Number</label>
                {isEditing ? (
                  <input
                    type="tel"
                    value={editData.phone}
                    onChange={(e) => handleInputChange('phone', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <Phone className="field-icon" />
                    <span>{profileData.phone}</span>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Date of Birth</label>
                {isEditing ? (
                  <input
                    type="date"
                    value={editData.dateOfBirth}
                    onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <Calendar className="field-icon" />
                    <span>{new Date(profileData.dateOfBirth).toLocaleDateString()}</span>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Location</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editData.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <MapPin className="field-icon" />
                    <span>{profileData.location}</span>
                  </div>
                )}
              </div>

              <div className="form-group full-width">
                <label>Bio</label>
                {isEditing ? (
                  <textarea
                    value={editData.bio}
                    onChange={(e) => handleInputChange('bio', e.target.value)}
                    rows="3"
                  />
                ) : (
                  <div className="form-value">
                    <span>{profileData.bio}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="emergency-contact">
            <h2>Emergency Contact</h2>
            <div className="details-form">
              <div className="form-group">
                <label>Contact Name</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editData.emergencyContact.name}
                    onChange={(e) => handleInputChange('emergencyContact.name', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <User className="field-icon" />
                    <span>{profileData.emergencyContact.name}</span>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Relationship</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editData.emergencyContact.relationship}
                    onChange={(e) => handleInputChange('emergencyContact.relationship', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <Heart className="field-icon" />
                    <span>{profileData.emergencyContact.relationship}</span>
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Phone Number</label>
                {isEditing ? (
                  <input
                    type="tel"
                    value={editData.emergencyContact.phone}
                    onChange={(e) => handleInputChange('emergencyContact.phone', e.target.value)}
                  />
                ) : (
                  <div className="form-value">
                    <Phone className="field-icon" />
                    <span>{profileData.emergencyContact.phone}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="profile-sidebar">
          <div className="achievements-section">
            <h3>Achievements</h3>
            <div className="achievements-list">
              {achievements.map((achievement) => (
                <div key={achievement.id} className={`achievement-card ${achievement.earned ? 'earned' : 'locked'}`}>
                  <div className="achievement-icon">{achievement.icon}</div>
                  <div className="achievement-content">
                    <h4>{achievement.title}</h4>
                    <p>{achievement.description}</p>
                    {achievement.earned ? (
                      <span className="achievement-date">Earned {achievement.date}</span>
                    ) : (
                      <div className="achievement-progress">
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{ width: `${(achievement.progress / 20) * 100}%` }}
                          ></div>
                        </div>
                        <span className="progress-text">{achievement.progress}/20</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="recent-activity">
            <h3>Recent Activity</h3>
            <div className="activity-list">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="activity-item">
                  <div className="activity-icon">{getActivityIcon(activity.type)}</div>
                  <div className="activity-content">
                    <h4>{activity.title}</h4>
                    <div className="activity-meta">
                      <span className="activity-date">{activity.date}</span>
                      {activity.duration && (
                        <span className="activity-duration">{activity.duration}</span>
                      )}
                      {activity.value && (
                        <span className="activity-value">{activity.value}</span>
                      )}
                      {activity.status && (
                        <span className={`activity-status ${activity.status}`}>
                          {activity.status}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;