// UpdatedNarrativeImpactDisplay.js

import React from 'react';
import { useGameState, useGameFunction, useGameDispatch } from '../../contexts/GameContext';
import './UpdatedNarrativeImpactDisplay.css'; 

const UpdatedNarrativeImpactDisplay = () => {
  const { selectedNarrative, secondaryNarrative, updatedFactCombination, isLoadingNews } = useGameState();
  const { setCurrentPhase } = useGameFunction(); 
  const dispatch = useGameDispatch();

  // Progress to outro phase of the game
  const handleContinue = () => {
    setCurrentPhase('outro'); 
    dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'CONCLUSION_WRAP_UP' });
  };
    
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
        disabled={isLoadingNews} 
      >
        Continue
      </button>
    </div>
  );
};

export default UpdatedNarrativeImpactDisplay;
