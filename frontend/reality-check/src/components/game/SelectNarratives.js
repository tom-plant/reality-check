// SelectedNarrative.js

import React from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import NarrativeBox from '../common/NarrativeBox'; 
import './SelectNarratives.css'; 


const SelectNarratives = () => {
  const { narrativeOptions, selectedNarrative } = useGameState();
  const dispatch = useGameDispatch();

  const handleNarrativeConfirmation = () => {
    // Logic to send selectedNarrative to backend
    // Implement this functionality
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'NARRATIVE_IMPACT' }); // Adjust the payload to the next phase's view name
    return
  };

  return (
    <div className="select-narratives">
        <h2>Select Narratives</h2>
        <div className="narratives-list">
          {narrativeOptions.map((narrative) => (
            <NarrativeBox 
              key={narrative.id} 
              narrative={narrative}
              isSelected={selectedNarrative && narrative.id === selectedNarrative.id}
              container="left"
            />
          ))}
        </div>
        <button 
          className="confirm-narrative" 
          disabled={!selectedNarrative} // Button is disabled if no narrative is selected
          onClick={handleNarrativeConfirmation} 
        >
          Confirm Narrative
      </button>
    </div>
  );
};

export default SelectNarratives;


