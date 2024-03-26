// IdentifyWeaknessesDisplay.js
import React from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import FactBox from '../common/FactBox'; 
import './IdentifyWeaknessesDisplay.css'; // Make sure to create a corresponding CSS file

const IdentifyWeaknessesDisplay = () => {
  const { updatedFactCombination, selectedFactCombination } = useGameState();
  const dispatch = useGameDispatch();
  const { identifyWeaknessesAndSetContent } = useGameFunction(); 

  const arraysAreEqual = (arr1, arr2) => {
    if (arr1.length !== arr2.length) return false;
    for (let i = 0; i < arr1.length; i++) {
      if (arr1[i].text !== arr2[i].text) return false; 
    }
    return true;
  };  

  const handleUpdateNarrative = () => {
    dispatch({ type: 'RESET_SELECTION_ENDED', payload: true });
    dispatch({ type: 'UPDATE_FACTS', payload: updatedFactCombination });
    console.log("updatedFactCombination in IdentifyWeaknessesDisplay is: ", updatedFactCombination);
    dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' }); // This will toggle the popup visibility
    identifyWeaknessesAndSetContent(updatedFactCombination);
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
        disabled={arraysAreEqual(updatedFactCombination, selectedFactCombination)}
      >
        Update Narrative
      </button>
    </div>
  );
};

export default IdentifyWeaknessesDisplay;
