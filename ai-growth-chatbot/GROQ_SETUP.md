# Groq API Setup Guide

## How to Fix "Invalid API Key" Error

The error `Groq error: Error code: 401 - {'error': {'message': 'Invalid API Key'}}` occurs when the Groq API key is missing, invalid, or not properly configured.

## Step-by-Step Setup

### 1. Get a Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key

### 2. Configure Environment Variables

Edit the `.env` file in the `backend/` directory:

```bash
# Open the .env file
cd ai-growth-chatbot/backend
# If the file doesn't exist, create it from the example:
cp .env.example .env
```

Add your Groq API key to the `.env` file:

```
GROQ_API_KEY="your_actual_groq_api_key_here"
GROQ_MODEL="llama3-70b-8192"
AI_PROVIDER="groq"
```

### 3. Restart the Server

After updating the `.env` file, restart your backend server:

```bash
# If using Flask development server
python app.py

# Or if using a process manager, restart the service
```

### 4. Verify the Configuration

The application will now:
- Use Groq as the primary AI provider
- Provide better error messages if the API key is invalid
- Fall back to OpenAI if Groq is unavailable (if configured)

## Troubleshooting

### Common Issues:

1. **API Key Format**: Ensure the key is properly formatted without extra spaces
2. **File Location**: The `.env` file must be in the `backend/` directory
3. **Server Restart**: Changes to `.env` require server restart
4. **Key Validity**: Verify the API key is active in your Groq console

### Error Messages:

- **"Missing GROQ_API_KEY"**: API key not set in environment variables
- **"Invalid GROQ_API_KEY"**: API key is incorrect or expired
- **401 Unauthorized**: Authentication failed with Groq API

## Alternative Setup

If you prefer to use OpenAI instead of Groq:

1. Set `AI_PROVIDER="openai"` in your `.env` file
2. Add `OPENAI_API_KEY="your_openai_api_key_here"`
3. Restart the server

The application will automatically switch to using OpenAI for AI responses.
