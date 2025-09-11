// API service for backend communication
const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  // Roundtable (conference) endpoints
  async getAllSessions() {
    // GET /roundtable/sessions - returns all sessions (hosted by user and others)
    return this.apiCall('/roundtable/sessions');
  }

  async createSession(sessionData) {
    // POST /roundtable/sessions - create a new session
    return this.apiCall('/roundtable/sessions', {
      method: 'POST',
      body: JSON.stringify(sessionData),
    });
  }

  async joinSession(sessionId) {
    // POST /roundtable/sessions/:id/join - join a session, notify conductor
    return this.apiCall(`/roundtable/sessions/${sessionId}/join`, {
      method: 'POST',
    });
  }

  async deleteSession(sessionId) {
    // DELETE /roundtable/sessions/:id - delete a session
    return this.apiCall(`/roundtable/sessions/${sessionId}`, {
      method: 'DELETE',
    });
  }
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
    const token = localStorage.getItem('token');

    console.log(`🔄 API Call: ${options.method || 'GET'} ${url}`);
    console.log('🔑 Token present:', !!token);

    const config = {
      headers: this.getAuthHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      let data;

      console.log(`📡 Response status: ${response.status} ${response.statusText}`);

      try {
        data = await response.json();
        console.log('📦 Response data:', data);
      } catch (jsonError) {
        console.warn('⚠️ Failed to parse JSON response:', jsonError);
        data = { success: false, message: `HTTP ${response.status}: ${response.statusText}` };
      }

      if (!response.ok) {
        const errorMessage = data.message || `HTTP ${response.status}: ${response.statusText}`;
        console.error('❌ API Error:', errorMessage);
        throw new Error(errorMessage);
      }

      return data;
    } catch (error) {
      console.error('💥 API call failed:', error);

      // Provide more specific error messages
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to server. Please check if the backend is running.');
      } else if (error.message.includes('401')) {
        throw new Error('Authentication error: Please log in again.');
      } else if (error.message.includes('403')) {
        throw new Error('Access denied: You do not have permission to access this resource.');
      } else if (error.message.includes('404')) {
        throw new Error('Not found: The requested resource was not found.');
      } else if (error.message.includes('500')) {
        throw new Error('Server error: Internal server error occurred.');
      }

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
    return this.apiCall('/pdf/upload', {
      method: 'POST',
      body: formData,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
  }

  // Request questions from uploaded PDF
  async getPdfQuestions(pdfPath) {
    return this.apiCall('/pdf/questions', {
      method: 'POST',
      body: JSON.stringify({ path: pdfPath }),
      headers: this.getAuthHeaders(),
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

  // Coding endpoints
  async getProjects() {
    return this.apiCall('/coding/projects');
  }

  async createProject(projectData) {
    return this.apiCall('/coding/projects', {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }

  async updateProject(projectId, projectData) {
    return this.apiCall(`/coding/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(projectData),
    });
  }

  async deleteProject(projectId) {
    return this.apiCall(`/coding/projects/${projectId}`, {
      method: 'DELETE',
    });
  }

  async getTemplates() {
    return this.apiCall('/coding/templates');
  }

  async createTemplate(templateData) {
    return this.apiCall('/coding/templates', {
      method: 'POST',
      body: JSON.stringify(templateData),
    });
  }

  async deleteTemplate(templateId) {
    return this.apiCall(`/coding/templates/${templateId}`, {
      method: 'DELETE',
    });
  }

  async getSnippets() {
    return this.apiCall('/coding/snippets');
  }

  async createSnippet(snippetData) {
    return this.apiCall('/coding/snippets', {
      method: 'POST',
      body: JSON.stringify(snippetData),
    });
  }

  async deleteSnippet(snippetId) {
    return this.apiCall(`/coding/snippets/${snippetId}`, {
      method: 'DELETE',
    });
  }

  // Code execution endpoints
  async executeCode(codeData) {
    return this.apiCall('/coding/execute', {
      method: 'POST',
      body: JSON.stringify(codeData),
    });
  }

  async getSupportedLanguages() {
    return this.apiCall('/coding/languages');
  }

  async validateCode(codeData) {
    return this.apiCall('/coding/validate', {
      method: 'POST',
      body: JSON.stringify(codeData),
    });
  }

  async executeSnippet(snippetId, inputData = '') {
    return this.apiCall(`/coding/snippets/${snippetId}/execute`, {
      method: 'POST',
      body: JSON.stringify({ input: inputData }),
    });
  }

  // Profile update method
  async updateProfile(profileData) {
    return this.apiCall('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  // Get user profile stats (placeholder - implement in backend)
  async getUserProfileStats() {
    return this.apiCall('/auth/profile/stats');
  }

  // Local Support endpoints
  async searchLocalSupport(location, serviceType = 'all') {
    const params = new URLSearchParams({
      location: location,
      service_type: serviceType
    });
    return this.apiCall(`/local-support/search?${params.toString()}`);
  }

  async getLocalSupportServiceTypes() {
    return this.apiCall('/local-support/service-types');
  }

  async getLocalSupportLocations() {
    return this.apiCall('/local-support/supported-locations');
  }

  // Logout
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
  }
}

export default new ApiService();
