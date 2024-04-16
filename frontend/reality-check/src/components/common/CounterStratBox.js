// CounterStratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './CounterStratBox.css'; 

const CounterStratBox = ({ counterstrat, isSelected, disabled, container}) => {
  const dispatch = useGameDispatch();
  const { selectedCounterStrat } = useGameState(); // Access the selected facts from context

  const toggleCounterStratSelection = () => {
    if (disabled) return; // Early return if interaction is disabled
  
    const actionType = isSelected ? 'DESELECT_COUNTERSTRAT' : 'SELECT_COUNTERSTRAT';
    dispatch({ type: actionType, payload: counterstrat });
  };


  return (
    <div 
      className={`counter-strat-box ${isSelected ? 'selected' : ''} ${container}`} 
      onClick={toggleCounterStratSelection}
    >
      {counterstrat.text}
    </div>
  );
};

export default CounterStratBox;