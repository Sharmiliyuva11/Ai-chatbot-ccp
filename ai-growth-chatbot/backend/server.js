const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Simple in-memory user storage (in production, use a database)
const users = [
  {
    id: 1,
    username: 'user',
    email: 'user@example.com',
    password: '123', // In production, this should be hashed
    name: 'Demo User'
  }
];

// Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Server is running' });
});

// Login endpoint
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;

  // Find user by email or username
  const user = users.find(u => 
    (u.email === email || u.username === email) && u.password === password
  );

  if (user) {
    // In production, generate a proper JWT token
    const token = `token_${user.id}_${Date.now()}`;
    
    res.json({
      success: true,
      message: 'Login successful',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        name: user.name
      },
      token
    });
  } else {
    res.status(401).json({
      success: false,
      message: 'Invalid credentials'
    });
  }
});

// Register endpoint
app.post('/api/auth/register', (req, res) => {
  const { name, email, password } = req.body;

  // Check if user already exists
  const existingUser = users.find(u => u.email === email);
  if (existingUser) {
    return res.status(400).json({
      success: false,
      message: 'User already exists'
    });
  }

  // Create new user
  const newUser = {
    id: users.length + 1,
    username: email.split('@')[0], // Use email prefix as username
    email,
    password, // In production, hash this password
    name
  };

  users.push(newUser);

  res.json({
    success: true,
    message: 'Registration successful',
    user: {
      id: newUser.id,
      username: newUser.username,
      email: newUser.email,
      name: newUser.name
    }
  });
});

// Get user profile
app.get('/api/user/profile', (req, res) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader) {
    return res.status(401).json({
      success: false,
      message: 'No authorization token provided'
    });
  }

  // Simple token validation (in production, use proper JWT validation)
  const token = authHeader.replace('Bearer ', '');
  const userId = token.split('_')[1];
  
  const user = users.find(u => u.id == userId);
  
  if (user) {
    res.json({
      success: true,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        name: user.name
      }
    });
  } else {
    res.status(401).json({
      success: false,
      message: 'Invalid token'
    });
  }
});

// Coding projects endpoints
app.get('/api/projects', (req, res) => {
  // Mock projects data
  const projects = [
    {
      id: 1,
      name: 'React Todo App',
      description: 'A simple todo application built with React and local storage.',
      language: 'JavaScript',
      framework: 'React',
      lastModified: '2 hours ago',
      status: 'active',
      files: 3,
      lines: 245
    },
    {
      id: 2,
      name: 'Python Data Analysis',
      description: 'Data analysis project using pandas and matplotlib.',
      language: 'Python',
      framework: 'Pandas',
      lastModified: '1 day ago',
      status: 'completed',
      files: 5,
      lines: 432
    }
  ];

  res.json({
    success: true,
    projects
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found'
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log('\nDemo credentials:');
  console.log('Username: user');
  console.log('Password: 123');
});

module.exports = app;