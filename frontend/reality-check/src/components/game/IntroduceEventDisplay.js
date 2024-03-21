// IntroduceEventDisplay.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import './IntroduceEventDisplay.css'; // Ensure you create and style this CSS file

const IntroduceEventDisplay = () => {
  const { selectedEvent, selectedNarrative, selectedFactCombination } = useGameState();
  const dispatch = useGameDispatch();
  const [contentLoaded, setContentLoaded] = useState(false);

  const handleContinue = () => {
    dispatch({ type: 'INTRODUCE_EVENT', payload: 'IDENTIFY_WEAKNESSES' }); // Adjust the payload to the next phase's view name
  };

  useEffect(() => {
    // Here you might want to set contentLoaded to true based on actual content loading status
    // For now, we'll simulate it with a timeout
    const timer = setTimeout(() => setContentLoaded(true), 2000); // Simulates content loading
    return () => clearTimeout(timer);
  }, []);

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
            <p>{selectedNarrative}</p>
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
      <button className="continue-button" onClick={handleContinue} disabled={!contentLoaded}>
        Continue
      </button>
    </div>
  );
};

export default IntroduceEventDisplay;
