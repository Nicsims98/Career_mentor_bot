import React from 'react'
import './PageStyles.css'
import './UserInput.css'

function UserInput() {
  return (
    <div className="page-container">
      <h2>User Profile</h2>
      <form className="user-form">
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
            <label htmlFor="interests">Interests</label>
            <textarea 
              id="interests" 
              name="interests" 
              placeholder="Enter your interests (e.g., Web Development, AI, Data Science)"
              rows="3"
            ></textarea>
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
    </div>
  )
}

export default UserInput
