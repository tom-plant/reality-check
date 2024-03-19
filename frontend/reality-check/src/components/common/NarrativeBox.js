// NarrativeBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './NarrativeBox.css'; 

const NarrativeBox = ({ narrative, isSelected, disabled, container}) => {
  const dispatch = useGameDispatch();
  const { selectedNarrative } = useGameState(); // Access the selected facts from context
  // Only allow selection if the fact is already selected or if less than 5 facts are selected

  const toggleNarrativeSelection = () => {
    if (disabled) return; // Early return if interaction is disabled
  
    const actionType = isSelected ? 'DESELECT_NARRATIVE' : 'SELECT_NARRATIVE';
    dispatch({ type: actionType, payload: narrative });
  };


  return (
    <div 
      className={`narrative-box ${isSelected ? 'selected' : ''} ${container}`} 
      onClick={toggleNarrativeSelection}
    >
      {narrative.text}
    </div>
  );
};

export default NarrativeBox;