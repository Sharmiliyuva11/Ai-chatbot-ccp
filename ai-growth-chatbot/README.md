# Coby - AI Growth Chatbot

A comprehensive AI-powered platform combining mental health support, coding tools, and community features.

## Features

- **Landing Page**: Welcome page with login and signup options
- **Authentication**: Login/Signup system with demo credentials
- **Dashboard**: Overview of user activities and statistics
- **Coding Space**: Integrated development environment for coding projects
- **Roundtable**: Group discussions and peer support sessions
- **Mind Space**: AI-powered mental health support
- **Speak Up**: Communication and feedback tools
- **Safe Link**: Secure resource sharing
- **Profile & Settings**: User management

## Demo Credentials

- **Username**: `user`
- **Password**: `123`

## Project Structure

```
ai-growth-chatbot/
├── frontend/          # React frontend application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing/       # Landing page
│   │   │   ├── Login/         # Login page
│   │   │   ├── Signup/        # Signup page
│   │   │   ├── Dashboard/     # Main dashboard
│   │   │   ├── CodingSpace/   # Code editor and projects
│   │   │   ├── Roundtable/    # Group sessions
│   │   │   └── ...
│   │   ├── components/
│   │   └── App.jsx
├── backend/           # Node.js backend server
│   ├── server.js      # Express server
│   └── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Frontend Setup

1. Navigate to the frontend directory:
   ```powershell
   cd "c:\Users\gace2\Desktop\sha\ccp\Ai-chatbot-ccp\ai-growth-chatbot\frontend"
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start the development server:
   ```powershell
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

### Backend Setup (Optional)

The frontend currently uses localStorage for authentication, but a backend server is also provided.

1. Navigate to the backend directory:
   ```powershell
   cd "c:\Users\gace2\Desktop\sha\ccp\Ai-chatbot-ccp\ai-growth-chatbot\backend"
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start the server:
   ```powershell
   npm start
   ```

   The backend will be available at `http://localhost:5000`

## Usage

1. **Access the Application**: Open your browser and go to `http://localhost:5173`

2. **Landing Page**: You'll see the landing page with information about Coby

3. **Sign Up**: Click "Get Started" or "Sign Up" to create a new account

4. **Sign In**: Use the demo credentials or click "Sign In" if you already have an account
   - Username: `user`
   - Password: `123`

5. **Dashboard**: After login, you'll be redirected to the dashboard

6. **Navigation**: Use the sidebar to navigate between different features:
   - **Dashboard**: Overview and statistics
   - **Coding Space**: Code editor with projects, templates, and snippets
   - **Roundtable**: Group discussion sessions
   - **Mind Space**: Mental health support
   - **Speak Up**: Communication tools
   - **Safe Link**: Resource sharing
   - **Profile**: User profile management
   - **Settings**: Application settings

## Key Features

### Coding Space
- **Projects**: Manage your coding projects
- **Templates**: Use pre-built project templates
- **Code Snippets**: Save and reuse code snippets
- **Code Editor**: Built-in code editor with syntax highlighting
- **Run Code**: Execute code (coming soon)

### Authentication
- **Protected Routes**: Pages require authentication
- **Session Management**: Login state persisted in localStorage
- **Logout**: Clear session and redirect to landing page

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Touch-friendly navigation

## Development

### Frontend Technologies
- **React 19**: Frontend framework
- **React Router**: Client-side routing
- **Vite**: Build tool and dev server
- **Lucide React**: Icon library
- **CSS3**: Styling with modern features

### Backend Technologies
- **Node.js**: Runtime environment
- **Express.js**: Web framework
- **CORS**: Cross-origin resource sharing
- **Body Parser**: Request parsing middleware

## API Endpoints (Backend)

- `GET /api/health` - Health check
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/user/profile` - Get user profile
- `GET /api/projects` - Get coding projects

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the ISC License.

## Support

For support or questions, please contact the development team or create an issue in the repository.