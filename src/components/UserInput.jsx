import React, { useState } from 'react'
import './PageStyles.css'
import './UserInput.css'
import { useNavigate } from 'react-router-dom';
import Roadmap from './Roadmap';


function UserInput() {
  const [selectedInterest, setSelectedInterest] = useState('');
  const [showRoadmap, setShowRoadmap] = useState(false);
  const [showVideo, setShowVideo] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    const userData = Object.fromEntries(formData.entries());
    
    // Log the collected data
    console.log('User Profile Data:', userData);

    // Show video
  setShowVideo(true);
  // Navigate after delay
  setTimeout(() => {
    if (selectedInterest) {
      // Navigate to "coming soon" for "other", regular roadmap for specific interests
      const path = selectedInterest === 'other' ? '/roadmap?type=coming-soon' : `/roadmap?type=${selectedInterest}`;
      navigate(path);
    }
  }, 3000);
    
    // You can add API call here later to send data to backend
    alert('Profile submitted successfully!');

    if (selectedInterest && selectedInterest !== 'other') {
      setShowRoadmap(true);
      // Navigate to roadmap page with the selected interest
      navigate(`/roadmap?type=${selectedInterest}`);
    }
    
    // Optionally clear the form
    e.target.reset();
    setSelectedInterest(''); // Reset the interest selection state
  };

  return (
    <div className="user-input-container">
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Personal Information</h3>
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input type="text" id="name" name="name" required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" name="email" required />
          </div>
        </div>

        <div className="form-section">
          <h3>Professional Information</h3>
          <div className="form-group">
            <label htmlFor="workType">Work Type</label>
            <select id="workType" name="workType" required>
              <option value="">Select work type</option>
              <option value="fullTime">Full-time</option>
              <option value="partTime">Part-time</option>
              <option value="freelance">Freelance</option>
              <option value="student">Student</option>
            </select>
          </div>
        </div>

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
              required
            >
              <option value="">Select your primary interest</option>
              <option value="software">Software Development</option>
              <option value="data">Data Analytics</option>
              <option value="uiux">UI/UX Design</option>
              <option value="project">Project Management</option>
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

        <button type="submit" className="submit-button">Submit</button>
      </form>

      {showRoadmap && selectedInterest && selectedInterest !== 'other' && (
        <Roadmap type={selectedInterest} />
      )}
    </div>
  );
}

export default UserInput;