// SelectedNarrative.js

import React from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import NarrativeBox from '../common/NarrativeBox'; 
import './SelectNarratives.css'; 


const SelectNarratives = () => {
  const { narrativeOptions, selectedNarrative } = useGameState();


  const handleNarrativeConfirmation = () => {
    // Logic to send selectedNarrative to backend
    // Implement this functionality
    console.log('Narrative confirmed:', selectedNarrative);
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



//Within your game phase components (e.g., SelectFacts, SelectNarratives), 
// use the passed goToNextPhase function to transition to the next phase upon certain actions, 
// like selecting a fact or confirming a narrative.