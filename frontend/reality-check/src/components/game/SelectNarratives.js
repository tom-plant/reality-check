// SelectedNarrative.js

import React from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import NarrativeBox from '../common/NarrativeBox'; 
import './SelectNarratives.css'; 


const SelectNarratives = () => {
  const { narrativeOptions, selectedNarrative, isLoadingNarratives } = useGameState();
  const dispatch = useGameDispatch();

  if (isLoadingNarratives) {
    console.log('loading narratives')
    return <div>Loading narratives...</div>; // Or any other loading indicator you prefer
  }

  console.log(narrativeOptions);

  const handleNarrativeConfirmation = () => {
    // Logic to send selectedNarrative to backend
    // Implement this functionality
    console.log(narrativeOptions);
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'NARRATIVE_IMPACT' }); 
    return
  };

  return (
    <div className="select-narratives">
        <h2>Select Narratives</h2>
        <div className="narratives-list">
          {narrativeOptions && narrativeOptions.map((narrative) => (
            <NarrativeBox 
              key={narrative.id} 
              narrative={narrative}
              isSelected={selectedNarrative && narrative === selectedNarrative}
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


