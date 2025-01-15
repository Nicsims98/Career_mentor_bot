import React, { useState, useEffect, useRef } from 'react'
import Sage from '../images/Sage logo.png'
import './Chatbox.css'

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // Add initial Sage message when component mounts
    setMessages([{
      text: "Hello! Type any question you have. I'm here to help you.",
      sender: 'sage'
    }]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    // Add user message immediately
    setMessages(prev => [...prev, { 
        text: newMessage, 
        sender: 'user' 
    }]);
    setIsLoading(true);

    try {
        const response = await fetch(import.meta.env.VITE_API_URL || 'http://localhost:5000/api/sage/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: newMessage }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            const errorMessage = errorData.error || 'Server error occurred';
            console.error('Chat API error:', errorMessage);
            throw new Error(errorMessage);
        }

        const data = await response.json();
        
        // Add Sage's response
        setMessages(prev => [...prev, { 
            text: data.response, 
            sender: 'sage' 
        }]);

    } catch (error) {
        console.error('Chat error:', error);
        let errorMessage = error.message;
        
        // Provide more user-friendly error messages
        if (errorMessage.includes('OpenAI API key not configured')) {
            errorMessage = 'The AI service is not properly configured. Please contact support.';
        } else if (errorMessage.includes('Invalid OpenAI API key')) {
            errorMessage = 'There is an authentication issue with the AI service. Please contact support.';
        } else if (error.message === 'Failed to fetch') {
            errorMessage = 'Unable to connect to the chat service. Please check your internet connection or try again later.';
        }
        
        setMessages(prev => [...prev, { 
            text: errorMessage,
            sender: 'sage' 
        }]);
    } finally {
        setIsLoading(false);
        setNewMessage('');
    }
  };

  return (
    <div className="chatbox-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`message-wrapper ${message.sender === 'sage' ? 'sage' : 'user'}`}
          >
            {message.sender === 'sage' && (
              <img src={Sage} alt="Sage" className="sage-avatar" />
            )}
            <div className="message-bubble">
              {message.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper sage">
            <img src={Sage} alt="Sage" className="sage-avatar" />
            <div className="message-bubble">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
          disabled={isLoading}
        />
        <button type="submit" className="send-button" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  )
}

export default Chatbox
