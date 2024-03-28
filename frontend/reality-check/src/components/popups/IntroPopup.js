import React, { useEffect, useState } from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext';
import './IntroPopup.css'; 

const IntroPopup = () => {
  const { } = useGameState();
  const dispatch = useGameDispatch();
  const [currentScreen, setCurrentScreen] = useState(0); 

  const screens = [
    { id: 1, text: "Instructions: ..." },
    { id: 2, text: "Briefing: ..." },
    { id: 3, text: "Fact Selection Instructions: ..." },
  ];

  const screenContent = screens[currentScreen].text;

  const handleNext = () => {
    if (currentScreen < screens.length - 1) { 
      setCurrentScreen(currentScreen + 1);
    }
  };

  const handlePrev = () => {
    if (currentScreen > 0) { 
      setCurrentScreen(currentScreen - 1);
    }
  };

  // Close popup 
  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_INTRO_POPUP' }); 
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <p>{screenContent}</p>
        {currentScreen > 0 && (
          <button className="prev-button" onClick={handlePrev}>
            Previous
          </button>
        )}
        {currentScreen < screens.length - 1 ? (
          <button className="next-button" onClick={handleNext}>
            Next
          </button>
        ) : (
          <button className="start-button" onClick={handleContinue}>
            Start
          </button>
        )}
      </div>
    </div>
  );
  
};

export default IntroPopup;