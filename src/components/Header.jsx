import { Link } from "react-router-dom";
import { useState } from "react";
import Sage from '../images/Sage.png'
import './Header.css'

function Header({ theme, toggleTheme }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <header className="header">
      <nav className="navbar">
        <div className="nav-left">
          <Link to="/chatbox" className="logo-link">
            <img 
              src={Sage} 
              alt="Sage-Career mentor bot" 
              className="logo"
            />
          </Link>
          <Link to='/' className="title">VSNE</Link>
        </div>
        
        <div className="nav-right">
          <button className="menu-toggle" onClick={toggleMenu}>
            <span className={`hamburger ${isMenuOpen ? 'open' : ''}`}></span>
          </button>
          
          <div className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
            <ul className="nav-links">
              <li>
                <Link to="/home" onClick={closeMenu}>Home</Link>
              </li>
              <li>
                <Link to="/userinput" onClick={closeMenu}>User Input</Link>
              </li>
              <li>
                <Link to="/roadmap" onClick={closeMenu}>Roadmap</Link>
              </li>
              <li>
                <Link to="/chatbox" onClick={closeMenu}>Chat with Sage</Link>
              </li>
              <li className="theme-toggle-item">
                <button onClick={toggleTheme} className="theme-toggle">
                  {theme === 'light' ? '🌙' : '☀️'}
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  )
}

export default Header
