// IntroduceEventDisplay.js

import React from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import './IntroduceEventDisplay.css'; 

const IntroduceEventDisplay = () => {
  const { selectedEvent, selectedNarrative, selectedFactCombination, isLoadingNews } = useGameState();
  const { setCurrentPhase } = useGameFunction(); 
  const dispatch = useGameDispatch();

  // Progress to next game phase
  const handleContinue = () => {
    setCurrentPhase('turn-point'); 
    dispatch({ type: 'SET_CURRENT_TURN_POINT_VIEW', payload: 'ALERT' });
  };

  return (
    <div className="introduce-event-display-container">
      <div className="introduce-event-display">
        <h2>Your Event</h2>
        {selectedEvent && (
          <div className="selected-event">
            <p>{selectedEvent.text}</p>
          </div>
        )}
        <h2>Your Narrative</h2>
        {selectedNarrative && (
          <div className="selected-narrative">
            <p>{selectedNarrative.text}</p>
          </div>
        )}
        <h2>Your Facts</h2>
        <div className="facts-list">
          {selectedFactCombination.map((fact) => (
            <div key={fact.id} className="displayed-fact">
              {fact.text}
            </div>
          ))}
        </div>
      </div>
      <button className="continue-button" onClick={handleContinue} disabled={isLoadingNews}>
        Continue
      </button>
    </div>
  );
};

export default IntroduceEventDisplay;
