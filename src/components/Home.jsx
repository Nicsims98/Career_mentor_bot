import Sage from '../images/Sage.png'
import './Home.css'
import { useNavigate } from 'react-router-dom'

function Home(){
    const navigate = useNavigate();

    const handleImageClick = () => {
        navigate('/chatbox');
    };

    return(
        <div className="home-container">
            <div className="home-content">
                <div className="image-container">
                    <img 
                        src={Sage} 
                        alt="Sage-Career mentor bot" 
                        className="home-logo"
                        onClick={handleImageClick}
                    />
                    <div className="speech-bubble">Hello! I'm Sage. How can I help?</div>
                </div>
                <div className="text-container">
                    <h1>VSNE</h1>
                    <div className="info-section">
                        <h2>About Sage</h2>
                        <p>
                            Sage is your AI-powered career mentor, designed to guide you through your professional journey.
                            Whether you're starting your career, looking to switch paths, or seeking advancement,
                            Sage provides personalized advice and structured roadmaps tailored to your goals.
                        </p>

                        <h2>How to Use VSNE</h2>
                        <ol className="steps-list">
                            <li>
                                <strong>Create Your Profile:</strong> Start by visiting the User Input page to tell us about 
                                your background, skills, and career aspirations.
                            </li>
                            <li>
                                <strong>Explore Career Roadmaps:</strong> Check out the Roadmap page for detailed, 
                                step-by-step guides to various career paths, complete with resources and learning materials.
                            </li>
                            <li>
                                <strong>Chat with Sage:</strong> Have questions? Click on Sage's image or the Chat with Sage 
                                option to start a conversation. Sage can help with:
                                <ul>
                                    <li>Career path recommendations</li>
                                    <li>Skill development advice</li>
                                    <li>Industry insights</li>
                                    <li>Job search strategies</li>
                                </ul>
                            </li>
                        </ol>

                        <h2>Features</h2>
                        <ul className="features-list">
                            <li>Personalized career guidance</li>
                            <li>Interactive career roadmaps</li>
                            <li>Real-time chat assistance</li>
                            <li>Comprehensive resource links</li>
                            <li>Progress tracking</li>
                        </ul>

                        <p className="get-started">
                            Ready to begin? Click on Sage or head to the User Input page to start your journey!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home
