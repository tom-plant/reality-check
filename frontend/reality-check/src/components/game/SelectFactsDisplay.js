// SelectFactsDisplay.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import FactBox from '../common/FactBox'; 
import './SelectFactsDisplay.css';

const SelectFactsDisplay = () => {
  const { selectedFactCombination, selectionEnded } = useGameState();
  const dispatch = useGameDispatch();

  const handleGenerateNarrative = () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_NARRATIVES' });
  };

  return (
    <div className="select-facts-display">
      <div className="spacer"></div>
      <div className="facts-list">
        {selectedFactCombination.map((fact) => (
          <FactBox 
            key={fact.id}
            fact={fact}
            isSelected={true} // These are always selected
            disabled={selectionEnded} 
            container="right"
          />
        ))}
      </div>
      <button className="generate-narrative" 
        disabled={!selectionEnded}
        onClick={handleGenerateNarrative}>
        Generate Narrative
      </button>
    </div>
  );
};


export default SelectFactsDisplay;






