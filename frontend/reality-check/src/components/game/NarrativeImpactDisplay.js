// NarrativeImpactDisplay.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import './NarrativeImpactDisplay.css'; // Make sure to create and style this CSS file

const NarrativeImpactDisplay = () => {
  const { selectedNarrative, selectedFactCombination } = useGameState();
  const dispatch = useGameDispatch();
  const [contentLoaded, setContentLoaded] = useState(false); // Simulate news content loading


  const handleContinue = () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_UPDATED_FACTS' });
  };

    // Simulate content loading completion after a delay. CHANGE THIS TO APPEAR ONLY ONCE NEWS ARTICLES HAVE LOADED IN
    useEffect(() => {
      const timer = setTimeout(() => setContentLoaded(true), 2000); // 2 seconds delay for simulation
      return () => clearTimeout(timer);
    }, []);

    
  return (
    <div className="narrative-impact-display-container">
      <div className="narrative-impact-display">
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
      <button
        className="continue-button"
        onClick={handleContinue}
        disabled={!contentLoaded} // Button is disabled until content is loaded
      >
        Continue
      </button>
    </div>
  );
};

export default NarrativeImpactDisplay;
