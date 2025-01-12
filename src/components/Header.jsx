import { Link } from "react-router-dom";
import Sage from '../images/Sage.png'
import './Header.css'

function Header({ theme, toggleTheme }) {
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
          <ul className="nav-links">
            <li>
              <Link to="/home">Home</Link>
            </li>
            <li>
              <Link to="/userinput">User Input</Link>
            </li>
            <li>
              <Link to="/roadmap">Roadmap</Link>
            </li>
            <li>
              <Link to="/chatbox">Chat with Sage</Link>
            </li>
          </ul>
          <button onClick={toggleTheme} className="theme-toggle">
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>
      </nav>
    </header>
  )
}

export default Header
