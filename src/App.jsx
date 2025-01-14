import { Routes, Route, useSearchParams } from 'react-router-dom';
import { useState, useEffect } from 'react'
import Home from './components/Home'
import Header from './components/Header'
import UserInput from './components/UserInput'
import Roadmap from './components/Roadmap'
import Chatbox from './components/Chatbox'
import './App.css'
import './styles/themes.css'

function App() {
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.body.className = theme === 'light' ? 'light-theme' : '';
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  return (
    <div className={theme === 'light' ? 'light-theme' : ''}>
      <Header theme={theme} toggleTheme={toggleTheme} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/userinput" element={<UserInput />} />
        <Route 
          path="/roadmap" 
          element={
            <RoadmapWrapper />
          } 
        />
        <Route path="/chatbox" element={<Chatbox />} />
      </Routes>
    </div>
  );
}

// Create a wrapper component to handle the URL parameters
function RoadmapWrapper() {
  const [searchParams] = useSearchParams();
  let type = searchParams.get('type');
  
  if (type === 'coming-soon') {
    return (
      <div className="roadmap-container">
        <h2>Roadmap Coming Soon!</h2>
        <p>We're working on creating more learning paths. Check back later!</p>
      </div>
    );
  }

  return <Roadmap type={type || 'software'} />;
}

export default App;
