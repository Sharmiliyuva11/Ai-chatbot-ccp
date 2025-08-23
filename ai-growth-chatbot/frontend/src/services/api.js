// API service for backend communication
const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  // Get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  // Generic API call method with resilient JSON handling
  async apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      let data;
      try {
        data = await response.json();
      } catch (_) {
        data = { success: false, message: `HTTP ${response.status}` };
      }

      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async register(userData) {
    return this.apiCall('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials) {
    const response = await this.apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.success && response.token) {
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      localStorage.setItem('isAuthenticated', 'true');
    }

    return response;
  }

  async getProfile() {
    return this.apiCall('/auth/profile');
  }

  // Password reset endpoints
  async forgotPassword(data) {
    return this.apiCall('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async verifyResetToken(data) {
    return this.apiCall('/auth/verify-reset-token', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async resetPassword(data) {
    return this.apiCall('/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Google OAuth endpoints
  async googleAuth() {
    return this.apiCall('/auth/google');
  }

  // Change password (for logged-in users)
  async changePassword(data) {
    return this.apiCall('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Chatbot endpoints
  async sendMessage(message) {
    return this.apiCall('/chatbot/message', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async analyzeSentiment(message) {
    return this.apiCall('/chatbot/sentiment', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async evaluateGrammar(audioFile) {
    const formData = new FormData();
    formData.append('audio', audioFile);

    return this.apiCall('/chatbot/grammar/evaluate', {
      method: 'POST',
      body: formData,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
  }

  // Generic file upload
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    return this.apiCall('/chatbot/upload', {
      method: 'POST',
      body: formData,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
  }

  // Reminder endpoints
  async getReminders() {
    return this.apiCall('/reminder/');
  }

  async addReminder(reminderData) {
    return this.apiCall('/reminder/', {
      method: 'POST',
      body: JSON.stringify(reminderData),
    });
  }

  async deleteReminder(reminderId) {
    return this.apiCall(`/reminder/${reminderId}`, {
      method: 'DELETE',
    });
  }

  // MindSpace endpoints
  async getMindSpaceSessions() {
    return this.apiCall('/mindspace/sessions');
  }

  async getMindSpaceCategories() {
    return this.apiCall('/mindspace/categories');
  }

  // Logout
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
  }
}

export default new ApiService();