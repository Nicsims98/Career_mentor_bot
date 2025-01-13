import React from 'react'
import './Roadmap.css'

const Roadmap = ({ type }) => {
  const roadmapData = {
    data: [
      { text: "Learn Excel & Google Sheets", link: "https://www.linkedin.com/learning/google-sheets-essential-training" },
      { text: "Understand SQL", link: "https://www.coursera.org/learn/sql-for-data-science" },
      { text: "Statistics & Probability", link: "https://www.khanacademy.org/math/statistics-probability" },
      { text: "Learn Data Visualization", link: "https://www.coursera.org/specializations/data-visualization" },
      { text: "Python for Data Analytics", link: "https://www.coursera.org/learn/python-data-analysis" },
      { text: "Data Cleaning & Wrangling", link: "https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet-data-wrangling-in-python" },
      { text: "Exploratory Data Analysis (EDA)", link: "https://www.youtube.com/watch?v=r-uOLxNrNk8" },
      { text: "Learn Machine Learning Basics", link: "https://www.geeksforgeeks.org/machine-learning/" },
      { text: "Work on Real-world Projects", link: "https://github.com/" },
      { text: "Build a Portfolio", link: "https://www.coursera.org/learn/applied-data-science-capstone" }
    ],
    software: [
      { text: "Learn a Programming Language", link: "https://www.coursera.org/specializations/java-programming" },
      { text: "Understand Data Structures & Algorithms", link: "https://www.coursera.org/specializations/data-structures-algorithms" },
      { text: "Learn Version Control (Git & GitHub)", link: "https://www.youtube.com/watch?v=SWYqp7iY_Tc" },
      { text: "Build Problem-solving Skills", link: "https://leetcode.com/" },
      { text: "Understand Databases", link: "https://datasciencedojo.com/blog/understanding-databases/" },
      { text: "Learn Web Development", link: "https://www.codecademy.com/catalog/subject/web-development" },
      { text: "Understand APIs", link: "https://www.linkedin.com/learning/designing-restful-apis" },
      { text: "Learn Software Design Principles", link: "https://www.youtube.com/playlist?list=PLrhzvIcii6GNjpARdnO4ueTUAVR9eMBpc" },
      { text: "Deploy Applications", link: "https://aws.amazon.com/getting-started/" },
      { text: "Contribute to Open-source", link: "https://github.com/topics/good-first-issue" }
    ],
    uiux: [
      { text: "Learn Design Principles", link: "https://www.edx.org/learn/graphic-design" },
      { text: "Master Design Tools", link: "https://www.youtube.com/watch?v=68w2VwalD5w" },
      { text: "Understand User Research", link: "https://careerfoundry.com/en/blog/ux-design/the-importance-of-user-research-and-how-to-do-it/" },
      { text: "Learn Wireframing & Prototyping", link: "https://www.codecademy.com/learn/intro-to-ui-ux/modules/ui-and-ux-prototyping-with-figma/cheatsheet" },
      { text: "Understand Visual Design", link: "https://www.interaction-design.org/literature/topics/visual-design" },
      { text: "Focus on Interaction Design", link: "https://www.coursera.org/specializations/interaction-design" },
      { text: "Learn Accessibility Standards", link: "https://www.w3.org/WAI/standards-guidelines/wcag/" },
      { text: "Study UX Writing", link: "https://app.uxcel.com/courses/ux-writing" },
      { text: "Create a Design System", link: "https://www.figma.com/blog/design-systems-102-how-to-build-your-design-system/" },
      { text: "Build a Portfolio", link: "https://www.behance.net/onboarding" }
    ],
    project: [
      "Understand Project Management Basics",
      "Master Project Management Methodologies",
      "Learn Task & Resource Management",
      "Master Communication Skills",
      "Learn Risk Management",
      "Focus on Budget & Cost Management",
      "Understand Quality Management",
      "Track & Report Project Progress",
      "Get Certified",
      "Lead a Real Project"
    ]
  };

  const getRoadmapContent = () => {
    const steps = roadmapData[type];
    if (!steps) return <div className='no-roadmap'>Invalid roadmap type</div>;

    const titles = {
      data: "Data Analytics Roadmap",
      software: "Software Engineering Roadmap",
      uiux: "UI/UX Design Roadmap",
      project: "Project Management Roadmap"
    };

    return (
      <div className="roadmap-section">
        <h3>{titles[type]}</h3>
        <div className="roadmap-steps">
          {steps.map((step, index) => (
            <div key={index} className="roadmap-step">
              <div className="step-number">{index + 1}</div>
              <div className="step-content">
                {step.link ? (
                  <a 
                    href={step.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="step-link"
                  >
                    {step.text}
                  </a>
                ) : (
                  step.text || step
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="roadmap-container">
      {getRoadmapContent()}
    </div>
  );
};

export default Roadmap;
