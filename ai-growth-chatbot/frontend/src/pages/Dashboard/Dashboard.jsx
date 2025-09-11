import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Users, 
  MessageSquare, 
  Bell,
  Activity,
  Calendar,
  Target,
  Award
} from 'lucide-react';
import Chatbot from '../../components/Chatbot/Chatbot';
import ApiService from '../../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState([]);
  const [moodData, setMoodData] = useState([]);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dashboardStats, setDashboardStats] = useState({
    mood: 8,
    stress: 1
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch dashboard stats
      const statsResponse = await ApiService.getDashboardStats();
      if (statsResponse.success) {
        const { stats: dbStats } = statsResponse;
        setDashboardStats({
          mood: dbStats.mood || 8,
          stress: dbStats.stress || 1
        });
        
        // Update stats array with real data
        setStats([
          {
            title: 'Chat Sessions',
            value: dbStats.chatSessions.toString(),
            subtitle: 'Total conversations',
            icon: MessageSquare,
            color: 'blue',
            trend: dbStats.chatSessions > 0 ? '+12%' : '0%'
          },
          {
            title: 'Active Tasks',
            value: dbStats.activeTasks.toString(),
            subtitle: 'Pending operations',
            icon: Activity,
            color: 'orange',
            trend: dbStats.activeTasks > 0 ? '+5%' : '0%'
          },
          {
            title: 'Meditation',
            value: dbStats.meditationSessions.toString(),
            subtitle: 'Sessions completed',
            icon: Bell,
            color: 'purple',
            trend: '0%'
          },
          {
            title: 'Community',
            value: dbStats.communityGroups.toString(),
            subtitle: 'Groups joined',
            icon: Users,
            color: 'green',
            trend: '0%'
          }
        ]);
      }

      // Fetch mood data
      const moodResponse = await ApiService.getMoodData();
      if (moodResponse.success) {
        setMoodData(moodResponse.moodData);
      }

      // Fetch recent activity
      const activityResponse = await ApiService.getRecentActivity();
      if (activityResponse.success) {
        const formattedActivities = activityResponse.activities.map(activity => ({
          type: activity.title,
          time: formatActivityTime(activity.time),
          status: activity.status,
          color: activity.color
        }));
        setActivities(formattedActivities);
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Fallback to default data on error
      setStats([
        {
          title: 'Chat Sessions',
          value: '0',
          subtitle: 'Total conversations',
          icon: MessageSquare,
          color: 'blue',
          trend: '0%'
        },
        {
          title: 'Active Tasks',
          value: '0',
          subtitle: 'Pending operations',
          icon: Activity,
          color: 'orange',
          trend: '0%'
        },
        {
          title: 'Meditation',
          value: '0',
          subtitle: 'Sessions completed',
          icon: Bell,
          color: 'purple',
          trend: '0%'
        },
        {
          title: 'Community',
          value: '0',
          subtitle: 'Groups joined',
          icon: Users,
          color: 'green',
          trend: '0%'
        }
      ]);
      setMoodData([
        { day: 'Mon', value: 7 },
        { day: 'Tue', value: 8 },
        { day: 'Wed', value: 6 },
        { day: 'Thu', value: 9 },
        { day: 'Fri', value: 7 },
        { day: 'Sat', value: 8 },
        { day: 'Sun', value: 9 }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const formatActivityTime = (timeStr) => {
    try {
      const date = new Date(timeStr);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMins / 60);
      const diffDays = Math.floor(diffHours / 24);

      if (diffDays > 0) {
        return `${diffDays} DAY${diffDays > 1 ? 'S' : ''} AGO`;
      } else if (diffHours > 0) {
        return `${diffHours} HR${diffHours > 1 ? 'S' : ''} AGO`;
      } else {
        return `${Math.max(1, diffMins)} MIN${diffMins > 1 ? 'S' : ''} AGO`;
      }
    } catch {
      return timeStr;
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h2>Today's Mental Check</h2>
          <h1>Feeling Great</h1>
          <p>Good work so far</p>
        </div>
        <div className="hero-stats">
          <div className="stat-item">
            <span className="stat-value">{dashboardStats.mood}/10</span>
            <span className="stat-label">Mood</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{dashboardStats.stress}/10</span>
            <span className="stat-label">Stress</span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className={`stat-card ${stat.color}`}>
            <div className="stat-header">
              <stat.icon className="stat-icon" />
              <span className="stat-trend">{stat.trend}</span>
            </div>
            <div className="stat-content">
              <h3 className="stat-title">{stat.title}</h3>
              <p className="stat-subtitle">{stat.subtitle}</p>
              <div className="stat-value-large">{stat.value}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-card mood-chart">
          <div className="chart-header">
            <TrendingUp className="chart-icon" />
            <div>
              <h3>Weekly Mood Trends</h3>
              <p>Track your emotional wellbeing over time</p>
            </div>
          </div>
          <div className="mood-chart-container">
            {moodData.map((item, index) => (
              <div key={index} className="mood-bar">
                <div 
                  className="mood-bar-fill" 
                  style={{ height: `${item.value * 10}%` }}
                ></div>
                <span className="mood-day">{item.day}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-card activity-chart">
          <div className="chart-header">
            <Activity className="chart-icon" />
            <div>
              <h3>Weekly Activity</h3>
              <p>Your wellness activities throughout the week</p>
            </div>
          </div>
          <div className="activity-bars">
            {[65, 78, 45, 89, 67, 78, 92].map((value, index) => (
              <div key={index} className="activity-bar">
                <div 
                  className="activity-bar-fill" 
                  style={{ height: `${value}%` }}
                ></div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="bottom-section">
  <div className="insights-card mood-distribution-box">
          <h3>Mood Distribution</h3>
          <div className="mood-distribution">
            <div className="mood-circle">
              <div className="circle-chart">
                <div className="circle-segment excellent"></div>
                <div className="circle-segment good"></div>
                <div className="circle-segment okay"></div>
                <div className="circle-segment poor"></div>
              </div>
            </div>
            <div className="mood-legend">
              <div className="legend-item">
                <span className="legend-color excellent"></span>
                <span>Excellent 45%</span>
              </div>
              <div className="legend-item">
                <span className="legend-color good"></span>
                <span>Good 30%</span>
              </div>
              <div className="legend-item">
                <span className="legend-color okay"></span>
                <span>Okay 20%</span>
              </div>
              <div className="legend-item">
                <span className="legend-color poor"></span>
                <span>Poor 5%</span>
              </div>
            </div>
          </div>
        </div>

  <div className="progress-card daily-meditation-box">
          <h3>Daily Meditation</h3>
          <div className="progress-stats">
            <div className="progress-item">
              <span className="progress-label">Weekly Check-ins</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: '75%' }}></div>
              </div>
              <span className="progress-value">75%</span>
            </div>
            <div className="progress-item">
              <span className="progress-label">Community Engagement</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: '60%' }}></div>
              </div>
              <span className="progress-value">60%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity and Chatbot */}
      <div className="bottom-grid">
        <div className="activity-timeline">
          <h3>Recent Timeline</h3>
          <div className="timeline-list">
            {activities.map((activity, index) => (
              <div key={index} className={`timeline-item ${activity.status}`}>
                <div className={`timeline-dot ${activity.color}`}></div>
                <div className="timeline-content">
                  <p className="timeline-text">{activity.type}</p>
                  <span className="timeline-time">{activity.time}</span>
                </div>
                <button className={`timeline-btn ${activity.status}`}>
                  {activity.status === 'completed' ? 'Completed' : 'Pending'}
                </button>
              </div>
            ))}
          </div>
        </div>
        
  <div className="chatbot-section ai-assistant-box">
          <h3>AI Assistant</h3>
          <Chatbot />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;