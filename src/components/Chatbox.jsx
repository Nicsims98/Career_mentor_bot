import React, { useState, useEffect, useRef } from 'react'
import Sage from '../images/Sage logo.png'
import './Chatbox.css'

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      setMessages([...messages, { text: newMessage, sender: 'user' }]);
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
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
        />
        <button type="submit" className="send-button">
          Send
        </button>
      </form>
    </div>
  )
}

export default Chatbox
