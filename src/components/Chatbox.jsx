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
    if (newMessage.trim()) {
      // Add user message immediately
      setMessages(prev => [...prev, { text: newMessage, sender: 'user' }]);
      setIsLoading(true);
      
      try {
        const response = await fetch('http://localhost:5000/api/sage/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: newMessage,
            type: 'general'
          }),
        });
        

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Add Sage's response
        setMessages(prev => [...prev, { 
          text: data.response, 
          sender: 'sage' 
        }]);
      } catch (error) {
        console.error('Error:', error);
        setMessages(prev => [...prev, { 
          text: "I apologize, but I'm having trouble responding right now. Please try again later.", 
          sender: 'sage' 
        }]);
      } finally {
        setIsLoading(false);
        setNewMessage('');
      }
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
