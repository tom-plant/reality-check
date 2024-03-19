import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; // Adjust the path as needed
import './FactBox.css'; 

const FactBox = ({ fact, isSelected, disabled }) => {
  const dispatch = useGameDispatch();
  const { selectedFactCombination } = useGameState(); // Access the selected facts from context
  // Only allow selection if the fact is already selected or if less than 5 facts are selected

  const toggleFactSelection = () => {
    if (disabled) {
      // If interaction is disabled, prevent any changes
      return;
    }

    if (isSelected || selectedFactCombination.length < 5) {
      // Only allow selection if the fact is already selected or if less than 5 facts are selected
      const actionType = isSelected ? 'DESELECT_FACT' : 'SELECT_FACT';
      dispatch({ type: actionType, payload: fact });
    } else {
      // Optional: Provide feedback to the user that no more selections can be made
      alert("You can select a maximum of 5 facts.");
    }
  };


  return (
    <div 
      className={`fact-box ${isSelected ? 'selected' : ''}`} 
      onClick={toggleFactSelection}
    >
      {fact.text}
    </div>
  );
};

export default FactBox;