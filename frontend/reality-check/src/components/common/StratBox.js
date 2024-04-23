// StratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './StratBox.css'; 

const StratBox = ({ strat, isSelected }) => {
  const dispatch = useGameDispatch();
  const { selectedStrat } = useGameState(); // Access the selected strategies from context

  const toggleStratSelection = () => {
    let actionType, stratLimitReached;

    actionType = isSelected ? 'DESELECT_STRAT' : 'SELECT_STRAT';
    stratLimitReached = !isSelected && selectedStrat.length >= 2;

    if (!stratLimitReached) {
      dispatch({ type: actionType, payload: strat });
    } else {
      alert("You can select a maximum of 2 strats."); // Feedback for the user when the limit is reached
    }
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

