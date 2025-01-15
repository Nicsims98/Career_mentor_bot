import { useState } from 'react';
import Roadmap from './Roadmap';
import './CareerRoadmap.css';

const CareerRoadmap = () => {
  const [selectedInterest, setSelectedInterest] = useState('');
  const [otherInterest, setOtherInterest] = useState('');

  const interests = [
    { value: 'software', label: 'Software Development' },
    { value: 'data', label: 'Data Analytics' },
    { value: 'uiux', label: 'UI/UX Design' },
    { value: 'project', label: 'Project Management' },
    { value: 'other', label: 'Other' }
  ];

  const handleInterestChange = (e) => {
    setSelectedInterest(e.target.value);
    if (e.target.value !== 'other') {
      setOtherInterest('');
    }
  };

  const renderRoadmapContent = () => {
    if (!selectedInterest) {
      return <div className="select-prompt">Please select an interest to view its roadmap</div>;
    }

    if (selectedInterest === 'other') {
      return <div className="coming-soon">Roadmap Coming Soon!</div>;
    }

    return <Roadmap type={selectedInterest} />;
  };

  return (
    <div className="career-roadmap-container">
      <div className="interest-selector">
        <h2>Career Roadmap</h2>
        <div className="selector-group">
          <select 
            value={selectedInterest}
            onChange={handleInterestChange}
            className="interest-dropdown"
          >
            <option value="">Select your interest</option>
            {interests.map((interest) => (
              <option key={interest.value} value={interest.value}>
                {interest.label}
              </option>
            ))}
          </select>
          
          {selectedInterest === 'other' && (
            <input
              type="text"
              value={otherInterest}
              onChange={(e) => setOtherInterest(e.target.value)}
              placeholder="Please specify your interest"
              className="other-interest-input"
            />
          )}
        </div>
      </div>
      
      <div className="roadmap-content">
        {renderRoadmapContent()}
      </div>
    </div>
  );
};

export default CareerRoadmap; 