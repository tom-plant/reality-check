// IdentifyWeaknessesDisplay.js
import React from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import FactBox from '../common/FactBox'; 
import './IdentifyWeaknessesDisplay.css'; // Make sure to create a corresponding CSS file

const IdentifyWeaknessesDisplay = () => {
  const { updatedFactCombination } = useGameState();
  const dispatch = useGameDispatch();

  const handleUpdateNarrative = () => {
    // Logic to update the narrative based on the selected facts
    // This might involve sending the updated selection to the backend
    console.log(updatedFactCombination);
    dispatch({ type: 'UPDATE_NARRATIVE', payload: updatedFactCombination });


    // Optionally, navigate to the next phase of the game
    // dispatch({ type: 'SET_CURRENT_VIEW', payload: 'NEXT_PHASE_VIEW_NAME' });
  };

  return (
    <div className="identify-weaknesses-display">
      <div className="facts-list">
        {updatedFactCombination.map(fact => (
          <FactBox
            key={fact.id}
            fact={fact}
            isSelected={true} // These facts are always selected in this display
            disabled={false} 
            container="right"
          />
        ))}
      </div>
      <button
        className="update-narrative"
        onClick={handleUpdateNarrative}
      >
        Update Narrative
      </button>
    </div>
  );
};

export default IdentifyWeaknessesDisplay;
