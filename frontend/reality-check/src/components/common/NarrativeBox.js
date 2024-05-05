// NarrativeBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './NarrativeBox.css'; 

const NarrativeBox = ({ narrative, isSelected, disabled, container}) => {
  const dispatch = useGameDispatch();
  const { selectedNarrative, currentView, selectedCounterNarrative } = useGameState(); // Access the selected narrative and current view from context

  const toggleNarrativeSelection = () => {
    if (disabled) return; // Early return if interaction is disabled

    // Choose action type based on the current view and selection state
    let actionType = isSelected ? 'DESELECT_NARRATIVE' : 'SELECT_NARRATIVE';

    // Modify action types if the current view is UPDATED_NARRATIVE_IMPACT
    if (currentView === 'UPDATED_NARRATIVE_IMPACT') {
      actionType = isSelected ? 'DESELECT_COUNTERNARRATIVE' : 'SELECT_COUNTERNARRATIVE';
    }

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