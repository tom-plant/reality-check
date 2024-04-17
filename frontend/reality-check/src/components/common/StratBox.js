// StratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './StratBox.css'; 

const StratBox = ({ strat, isSelected, disabled}) => {
  const dispatch = useGameDispatch();
  const { selectedStrat } = useGameState(); // Access the selected facts from context

  const toggleStratSelection = () => {
    if (disabled) return; // Early return if interaction is disabled
  
    const actionType = isSelected ? 'DESELECT_STRAT' : 'SELECT_STRAT';
    dispatch({ type: actionType, payload: strat });
  };


  return (
    <div 
      className={`strat-box ${isSelected ? 'selected' : ''}`}
      onClick={toggleStratSelection}
    >
      {strat.text}
    </div>
  );
};

export default StratBox;