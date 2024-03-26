import React, { useState } from 'react';
import { useGameFunction, useGameState, useGameDispatch } from '../../contexts/GameContext'; // Adjust the import path as needed
import './AuthLogin.css'; 

const AuthLogin = ({ setCurrentIntroView }) => {
  const { loginUser, setCurrentLanguage} = useGameFunction();
  const [localUsername, setLocalUsername] = useState('');
  const [localEmail, setLocalEmail] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track login status
  const dispatch = useGameDispatch();
  const [bump, setBump] = useState(false); // State for bump animation


  const handleUsernameChange = (e) => {
    setLocalUsername(e.target.value);
  };

  const handleEmailChange = (e) => {
    setLocalEmail(e.target.value);
  };

  // Function to handle login click
  const loginClick = async () => {
    if (localUsername && localEmail) { // Check if both fields have content
      dispatch({ type: 'SET_USER', payload: localUsername });
      dispatch({ type: 'SET_EMAIL', payload: localEmail });
      await loginUser(localUsername, localEmail); // loginUser function from your context
      setIsLoggedIn(true); // Set login status to true upon successful login
    } else {
      // Trigger bump animation if fields are empty
      setBump(true);
      setTimeout(() => setBump(false), 200); // Reset bump animation
    }
  };

  const handleLanguageChange = (event) => {
    setCurrentLanguage(event.target.value); // Update the language in the context
  };

  return (
    <div className="auth-login">
      <h2>Register to Start</h2>
      <div className="input-container">
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={localUsername}
            onChange={handleUsernameChange}
          />
        </div>
        <div className="input-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={localEmail}
            onChange={handleEmailChange}
          />
        </div>
        <div className="input-group">
          <label htmlFor="language-select">Select Language</label>
          <select id="language-select" onChange={handleLanguageChange}>
            <option value="ENG">English</option>
            <option value="EST">Estonian</option>
            <option value="RUS">Russian</option>
          </select>
        </div>
      </div>
      <button
        className={`login ${bump ? 'bump' : ''}`}
        onClick={loginClick}
        disabled={isLoggedIn}
      >
        Login
      </button>
      <button className='proceed' onClick={() => setCurrentIntroView('EXPO_INBOX')} disabled={!isLoggedIn}>Start Game</button>
    </div>
  );
};

export default AuthLogin;
