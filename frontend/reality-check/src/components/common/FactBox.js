import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; // Adjust the path as needed
import './FactBox.css'; 

const FactBox = ({ fact, isSelected, disabled, container }) => {
  const dispatch = useGameDispatch();
  const { selectedFactCombination, currentView, updatedFactCombination } = useGameState();

  const toggleFactSelection = () => {
    if (disabled) {
      // If interaction is disabled, prevent any changes
      return;
    }

    let actionType, factLimitReached;

    // Check if we are in the IDENTIFY_WEAKNESSES phase
    if (currentView === 'IDENTIFY_WEAKNESSES') {
      actionType = isSelected ? 'DESELECT_UPDATED_FACT' : 'SELECT_UPDATED_FACT';
      factLimitReached = !isSelected && updatedFactCombination.length >= 5;
    } else {
      // Default to using SELECT_FACT / DESELECT_FACT for SELECT_FACTS phase with a 5 fact limit
      actionType = isSelected ? 'DESELECT_FACT' : 'SELECT_FACT';
      factLimitReached = !isSelected && selectedFactCombination.length >= 5;
    }

    if (!factLimitReached) {
      dispatch({ type: actionType, payload: fact });
    } else {
      alert("You can select a maximum of 5 facts."); // Feedback for the user when the limit is reached
    }
  };

  return (
    <div 
      className={`fact-box ${isSelected ? 'selected' : ''} ${container}`} 
      onClick={toggleFactSelection}
    >
      {fact.text}
    </div>
  );
};

export default FactBox;
