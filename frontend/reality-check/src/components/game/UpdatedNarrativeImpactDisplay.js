// UpdatedNarrativeImpactDisplay.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import './UpdatedNarrativeImpactDisplay.css'; // Make sure to create and style this CSS file

const UpdatedNarrativeImpactDisplay = () => {
  const { selectedNarrative, secondaryNarrative, updatedFactCombination } = useGameState();
  const dispatch = useGameDispatch();
  const [contentLoaded, setContentLoaded] = useState(false); // Simulate news content loading


  const handleContinue = () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'IDK_YET' });
  };

    // Simulate content loading completion after a delay. CHANGE THIS TO APPEAR ONLY ONCE NEWS ARTICLES HAVE LOADED IN
    useEffect(() => {
      const timer = setTimeout(() => setContentLoaded(true), 2000); // 2 seconds delay for simulation
      return () => clearTimeout(timer);
    }, []);

    
  return (
    <div className="updated-narrative-impact-display-container">
      <div className="updated-narrative-impact-display">
        <h2>Updated Narrative</h2>
          {secondaryNarrative && (
          <div className="secondary-narrative">
            <p>{secondaryNarrative.text}</p>
          </div>
        )}
        <h2>Original Narrative</h2>
        {selectedNarrative && (
        <div className="selected-narrative">
          <p>{selectedNarrative.text}</p>
        </div>
      )}
        <h2>Updated Facts</h2>
        <div className="facts-list">
          {updatedFactCombination.map((fact) => (
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

export default UpdatedNarrativeImpactDisplay;
