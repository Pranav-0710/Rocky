import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Loader2, Paperclip } from 'lucide-react';
import axios from 'axios';
import './ChatInterface.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const PIN_CODE = "0710"; // You can change this to any 4-digit code

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm Rocky, your AI assistant. How can I help you today?",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [pinInput, setPinInput] = useState('');
  const [pinError, setPinError] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isAuthenticated) {
      scrollToBottom();
    }
  }, [messages, isAuthenticated]);

  const handlePinSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (pinInput === PIN_CODE) {
      setIsAuthenticated(true);
      setPinError(false);
    } else {
      setPinError(true);
      setPinInput('');
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/chat`, {
        message: userMessage.text,
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.reply,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running.",
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/api/memory/upload`, formData);
      const successMessage: Message = {
        id: Date.now().toString(),
        text: `I've learned from "${file.name}". My memory is now sharper!`,
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, successMessage]);
    } catch (error) {
      console.error('File upload error:', error);
    } finally {
      setIsLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-logo">
            <img src="/logo.png" alt="Rocky Logo" />
          </div>
          <h2>Agent Rocky</h2>
          <p>Please enter your secure PIN</p>
          <form onSubmit={handlePinSubmit}>
            <input
              type="password"
              maxLength={4}
              placeholder="••••"
              value={pinInput}
              onChange={(e) => {
                setPinInput(e.target.value);
                setPinError(false);
              }}
              className={pinError ? 'error' : ''}
              autoFocus
            />
            {pinError && <span className="error-text">Incorrect PIN. Access Denied.</span>}
            <button type="submit">Unlock Ally</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>Rocky AI</h1>
        <div className="header-status">
          <div className={`status-dot ${isLoading ? 'loading' : 'online'}`}></div>
        </div>
      </header>

      <main className="messages-list">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
            <div className="message-bubble">
              {msg.text}
            </div>
            <div className="message-info">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper bot">
            <div className="message-bubble loading">
              <Loader2 className="animate-spin" size={18} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <footer className="input-area">
        <div className="input-wrapper">
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileUpload} 
            style={{ display: 'none' }} 
          />
          <button 
            className="icon-button" 
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
          >
            <Paperclip size={20} />
          </button>
          <input
            type="text"
            className="chat-input"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            disabled={isLoading}
          />
          <button 
            className="send-button" 
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            {isLoading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
          </button>
        </div>
      </footer>
    </div>
  );
};

export default ChatInterface;
