import React from 'react'
import './Roadmap.css'

function Roadmap() {
  const roadmapSteps = [
    { 
      color: '#FF6B6B', 
      text: 'Learn Programming Basics', 
      link: 'https://www.freecodecamp.org/',
      description: 'Start with fundamental concepts like variables, loops, and functions. Learn popular languages like Python or JavaScript.'
    },
    { 
      color: '#4ECDC4', 
      text: 'Master Core CS Concepts', 
      link: 'https://www.coursera.org/specializations/computer-fundamentals',
      description: 'Understand algorithms, data structures, and computer science theory to build a strong foundation.'
    },
    { 
      color: '#45B7D1', 
      text: 'Build Web Development Skills', 
      link: 'https://www.theodinproject.com/',
      description: 'Learn HTML, CSS, and JavaScript. Build responsive websites and understand web development principles.'
    },
    { 
      color: '#96CEB4', 
      text: 'Learn Framework (React)', 
      link: 'https://react.dev/',
      description: 'Master React.js for building modern user interfaces. Learn components, state management, and hooks.'
    },
    { 
      color: '#FFEEAD', 
      text: 'Practice Data Structures', 
      link: 'https://leetcode.com/',
      description: 'Solve coding challenges to improve problem-solving skills and prepare for technical interviews.'
    },
    { 
      color: '#D4A5A5', 
      text: 'Contribute to Open Source', 
      link: 'https://github.com/explore',
      description: 'Get real-world experience by contributing to open source projects. Learn Git and collaboration.'
    },
    { 
      color: '#9B59B6', 
      text: 'Build Portfolio Projects', 
      link: 'https://github.com/',
      description: 'Create personal projects to showcase your skills. Build full-stack applications.'
    },
    { 
      color: '#E67E22', 
      text: 'Learn System Design', 
      link: 'https://www.educative.io/path/scalability-system-design',
      description: 'Understand how to design scalable systems. Learn about databases, APIs, and architecture.'
    },
    { 
      color: '#58D68D', 
      text: 'Practice Interview Skills', 
      link: 'https://www.pramp.com/',
      description: 'Practice technical interviews, behavioral questions, and whiteboard coding challenges.'
    },
    { 
      color: '#5D6D7E', 
      text: 'Apply for Jobs', 
      link: 'https://www.linkedin.com/jobs/',
      description: 'Polish your resume, build your LinkedIn profile, and start applying for software engineering positions.'
    }
  ];

  return (
    <div className="roadmap-container">
      <h1 className="career-title">Software Engineer</h1>
      
      {/* Roadmap Visual */}
      <div className="roadmap-visual">
        <div className="road-line"></div>
        {roadmapSteps.map((step, index) => (
          <div 
            key={index} 
            className={`roadmap-pointer ${index % 2 === 0 ? 'top' : 'bottom'}`}
            style={{ left: `${(index + 1) * 9}%`, backgroundColor: step.color }}
          >
            <span className="pointer-text">{index + 1}</span>
          </div>
        ))}
      </div>

      {/* Roadmap Cards */}
      <div className="roadmap-cards">
        {roadmapSteps.map((step, index) => (
          <a 
            key={index}
            href={step.link}
            target="_blank"
            rel="noopener noreferrer"
            className="roadmap-card"
            style={{ borderColor: step.color }}
          >
            <span className="step-number" style={{ backgroundColor: step.color }}>
              {index + 1}
            </span>
            <div className="card-content">
              <p>{step.text}</p>
              <div className="card-description">{step.description}</div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}

export default Roadmap
