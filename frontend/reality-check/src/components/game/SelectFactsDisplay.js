// SelectFactsDisplay.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import FactBox from '../common/FactBox'; 
import './SelectFactsDisplay.css';

const SelectFactsDisplay = () => {
  const { selectedFactCombination, timerHasEnded, narrativeOptions } = useGameState();
  const { fetchAndSetNarratives } = useGameFunction(); 
  const dispatch = useGameDispatch();

  const handleGenerateNarrative = async () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_NARRATIVES' });
    await fetchAndSetNarratives(selectedFactCombination);
    dispatch({ type: 'COPY_FACTS_TO_UPDATED', payload: selectedFactCombination }); 
    dispatch({ type: 'RESET_SELECTION_ENDED' });
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
            disabled={timerHasEnded} 
            container="right"
          />
        ))}
      </div>
      <button className="generate-narrative" 
        disabled={!timerHasEnded}
        onClick={handleGenerateNarrative}>
        Generate Narrative
      </button>
    </div>
  );
};


export default SelectFactsDisplay;






