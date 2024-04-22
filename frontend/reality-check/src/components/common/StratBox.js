// StratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './StratBox.css'; 

const StratBox = ({ strat, isSelected, disabled}) => {
  const dispatch = useGameDispatch();
  const { selectedStrat } = useGameState(); // Access the selected facts from context

  const toggleStratSelection = () => {
    if (disabled || !strat) return; // Early return if interaction is disabled or strat is undefined
  
    const actionType = isSelected ? 'DESELECT_STRAT' : 'SELECT_STRAT';
    dispatch({ type: actionType, payload: strat });
  };

  // Check if strat is defined before rendering
  if (!strat) {
    console.error('StratBox received an undefined strat object.');
    return null; // Or render some fallback UI
  }

  return (
    <div 
      className={`strat-box ${isSelected ? 'selected' : ''} ${disabled ? 'disabled' : ''}`}
      onClick={toggleStratSelection}
    >
      {strat.text} // Safe to access text because of the check above
    </div>
  );
};

export default StratBox;