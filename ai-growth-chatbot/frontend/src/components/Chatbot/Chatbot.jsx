import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader, Mic, MicOff, Paperclip } from 'lucide-react';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI assistant. I can help you with coding questions, provide grammar feedback, and offer mental wellness support. How can I assist you today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null); // eslint-disable-line no-unused-vars
  const [uploadedPdfPath, setUploadedPdfPath] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const { default: ApiService } = await import('../../services/api');

      // If user asks any question mentioning both 'pdf' and 'question', call getPdfQuestions
      if (uploadedPdfPath && /pdf/i.test(inputMessage) && /question/i.test(inputMessage)) {
        const response = await ApiService.getPdfQuestions(uploadedPdfPath);
        if (response.success && response.questions) {
          const botMessage = {
            id: Date.now() + 1,
            text: Array.isArray(response.questions) ? response.questions.join('\n') : response.questions,
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, botMessage]);
        } else {
          const errorMessage = {
            id: Date.now() + 1,
            text: response.message || "Sorry, I couldn't generate questions from the PDF.",
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
        }
      } else if (uploadedPdfPath && /pdf/i.test(inputMessage) && /(summary|summarize|explain|overview)/i.test(inputMessage)) {
        // If user asks for summary/explanation of the PDF
        const response = await ApiService.apiCall('/pdf/explain', {
          method: 'POST',
          body: JSON.stringify({ path: uploadedPdfPath }),
          headers: ApiService.getAuthHeaders(),
        });
        if (response.success && response.summary) {
          const botMessage = {
            id: Date.now() + 1,
            text: response.summary,
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, botMessage]);
        } else if (response.success && response.explanation) {
          const botMessage = {
            id: Date.now() + 1,
            text: response.explanation,
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, botMessage]);
        } else {
          const errorMessage = {
            id: Date.now() + 1,
            text: response.message || "Sorry, I couldn't summarize or explain the PDF.",
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
        }
      } else {
        // Default: send message to chatbot
        let response;
        if (uploadedPdfPath) {
          response = await ApiService.sendPdfAnswer(uploadedPdfPath, inputMessage);
        } else {
          response = await ApiService.sendMessage(inputMessage);
        }

        if (response.success) {
          const replyText = response.response || response.answer;
          const botMessage = {
            id: Date.now() + 1,
            text: replyText,
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, botMessage]);
        } else {
          const errorMessage = {
            id: Date.now() + 1,
            text: response.message || "Sorry, I'm having trouble processing your request right now. Please try again later.",
            sender: 'bot',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting right now. Please check your connection and try again.",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-info">
          <Bot className="bot-icon" />
          <div>
            <h3>AI Assistant</h3>
            <span className="status">Online</span>
          </div>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-avatar">
              {message.sender === 'bot' ? <Bot size={20} /> : <User size={20} />}
            </div>
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              <div className="message-time">{formatTime(message.timestamp)}</div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-avatar">
              <Bot size={20} />
            </div>
            <div className="message-content">
              <div className="message-text typing">
                <Loader className="loading-icon" />
                Thinking...
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="message-input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="message-input"
          />

          {/* File upload button */}
          <button
            type="button"
            className="send-button"
            onClick={() => fileInputRef.current?.click()}
            title="Upload a file"
          >
            <Paperclip size={20} />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            style={{ display: 'none' }}
            onChange={async (e) => {
              const file = e.target.files?.[0];
              if (!file) return;
              setSelectedFile(file);
              const { default: api } = await import('../../services/api');
              try {
                const res = await api.uploadFile(file);
                if (res?.success && res?.path) {
                  setUploadedPdfPath(res.path);
                }
                const text = res?.success
                  ? `File “${res.filename}” uploaded successfully.`
                  : `Upload failed: ${res?.message || 'Unknown error'}`;
                setMessages((prev) => [
                  ...prev,
                  { id: Date.now() + 2, text, sender: 'bot', timestamp: new Date() },
                ]);
              } catch (err) {
                setMessages((prev) => [
                  ...prev,
                  { id: Date.now() + 3, text: `Upload error: ${err.message}`, sender: 'bot', timestamp: new Date() },
                ]);
              }
            }}
          />

          {/* Voice toggle */}
          <button
            type="button"
            className="send-button"
            title={isRecording ? 'Stop recording' : 'Start voice message'}
            onClick={async () => {
              try {
                if (!isRecording) {
                  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                  streamRef.current = stream;
                  const recorder = new MediaRecorder(stream);
                  mediaRecorderRef.current = recorder;
                  audioChunksRef.current = [];
                  recorder.ondataavailable = (e) => e.data && audioChunksRef.current.push(e.data);
                  recorder.onstop = async () => {
                    const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                    const file = new File([blob], `voice-${Date.now()}.webm`, { type: 'audio/webm' });
                    const { default: api } = await import('../../services/api');
                    try {
                      const res = await api.evaluateGrammar(file);
                      const text = res?.success
                        ? `Grammar analysis score: ${res.grammar_score ?? 'N/A'}. Issues: ${res.issues_found}.`
                        : `Grammar check failed: ${res?.message || res?.error || 'Unknown error'}`;
                      setMessages((prev) => [
                        ...prev,
                        { id: Date.now() + 4, text, sender: 'bot', timestamp: new Date() },
                      ]);
                    } catch (err) {
                      setMessages((prev) => [
                        ...prev,
                        { id: Date.now() + 5, text: `Grammar check error: ${err.message}`, sender: 'bot', timestamp: new Date() },
                      ]);
                    }
                    streamRef.current?.getTracks().forEach((t) => t.stop());
                    streamRef.current = null;
                  };
                  recorder.start();
                  setIsRecording(true);
                } else {
                  mediaRecorderRef.current?.stop();
                  setIsRecording(false);
                }
              } catch (err) {
                setIsRecording(false);
                setMessages((prev) => [
                  ...prev,
                  { id: Date.now() + 6, text: `Microphone error: ${err.message}`, sender: 'bot', timestamp: new Date() },
                ]);
              }
            }}
          >
            {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
          </button>

          {/* Send */}
          <button 
            type="submit" 
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;