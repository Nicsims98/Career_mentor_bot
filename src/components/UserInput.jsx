import React, { useState } from 'react'
import './PageStyles.css'
import './UserInput.css'

function UserInput() {
  const [showVideo, setShowVideo] = useState(false);
  const [selectedInterest, setSelectedInterest] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    const userData = Object.fromEntries(formData.entries());
    
    // Log the collected data (for now)
    console.log('User Profile Data:', userData);
    
    // You can add API call here later to send data to backend
    alert('Profile submitted successfully!');
    
    // Optionally clear the form
    e.target.reset();
  };

  const handleSpinningCat = () => {
    setShowVideo(true);
  };
  return (
    <div className="page-container">
      <h2>User Profile</h2>
      <form className="user-form" onSubmit={handleSubmit}>

        {/* Personal Information Section */}
        <div className="form-section">
          <h3>Personal Information</h3>
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input type="text" id="name" name="name" placeholder="Enter your full name" />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" name="email" placeholder="Enter your email address" />
          </div>
          
          <div className="form-group">
            <label htmlFor="age">Age</label>
            <input type="number" id="age" name="age" placeholder="Enter your age" min="10" max="100" />
          </div>
          
          <div className="form-group">
            <label htmlFor="workType">Preferred Work Type</label>
            <select id="workType" name="workType">
              <option value="">Select work type</option>
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">On-site</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input type="text" id="location" name="location" placeholder="Enter your location" />
          </div>
        </div>

        {/* Skills and Interests Section */}
        <div className="form-section">
          <h3>Skills & Interests</h3>
          <div className="form-group">
            <label htmlFor="skills">Skills</label>
            <textarea 
              id="skills" 
              name="skills" 
              placeholder="Enter your skills (e.g., Python, Creative Writing, Project Management)"
              rows="3"
            ></textarea>
          </div>
          
          <div className="form-group">
            <label htmlFor="interests">Primary Interest</label>
            <select 
              id="interests" 
              name="interests"
              value={selectedInterest}
              onChange={(e) => setSelectedInterest(e.target.value)}
            >
              <option value="">Select your primary interest</option>
              <option value="software">Software Development</option>
              <option value="data">Data Analytics</option>
              <option value="uiux">UI/UX Design</option>
              <option value="project">Project Management</option>
              <option value="finance">Finance</option>
              <option value="marketing">Marketing</option>
              <option value="other">Other</option>
            </select>
            {selectedInterest === 'other' && (
              <input
                type="text"
                id="otherInterest"
                name="otherInterest"
                placeholder="Please specify your interest"
                className="other-interest-input"
                style={{ marginTop: '10px' }}
              />
            )}
          </div>
        </div>

        {/* Education and Experience Section */}
        <div className="form-section">
          <h3>Education & Experience</h3>
          <div className="form-group">
            <label htmlFor="education">Education</label>
            <textarea 
              id="education" 
              name="education" 
              placeholder="Enter your educational background"
              rows="3"
            ></textarea>
          </div>
          
          <div className="form-group">
            <label htmlFor="experience">Work Experience</label>
            <textarea 
              id="experience" 
              name="experience" 
              placeholder="Enter your work experience (if any)"
              rows="3"
            ></textarea>
          </div>
        </div>

        {/* Career Goals Section */}
        <div className="form-section">
          <h3>Career Goals</h3>
          <div className="form-group">
            <label htmlFor="shortTerm">Short-term Goals</label>
            <textarea 
              id="shortTerm" 
              name="shortTerm" 
              placeholder="Enter your short-term career goals"
              rows="3"
            ></textarea>
          </div>
          
          <div className="form-group">
            <label htmlFor="longTerm">Long-term Goals</label>
            <textarea 
              id="longTerm" 
              name="longTerm" 
              placeholder="Enter your long-term career goals"
              rows="3"
            ></textarea>
          </div>
        </div>

        <button type="submit" className="submit-btn">Submit</button>
      </form>
      
      <button 
        onClick={handleSpinningCat} 
        className="spinning-cat-btn"
      >
        Spinning Cat
      </button>

      {showVideo && (
        <div className="video-modal-overlay">
          <div className="video-modal">
            <button 
              className="close-button"
              onClick={() => setShowVideo(false)}
            >
              ×
            </button>
            <video 
              controls 
              autoPlay
              src="/src/images/nethenoob vid.mp4"
              style={{ width: '100%', height: 'auto' }}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default UserInput
