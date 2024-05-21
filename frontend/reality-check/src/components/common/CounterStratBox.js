// CounterStratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './CounterStratBox.css'; 

const CounterStratBox = ({ counterstrat, isSelected, disabled, container, maxSelection = 2 }) => {
  const dispatch = useGameDispatch();
  const { selectedCounterStrat } = useGameState(); // Access the selected facts from context

  const toggleCounterStratSelection = () => {
    if (disabled) return; // Early return if interaction is disabled

    let actionType, counterStratLimitReached;

    actionType = isSelected ? 'DESELECT_COUNTERSTRAT' : 'SELECT_COUNTERSTRAT';
    counterStratLimitReached = !isSelected && selectedCounterStrat.length >= maxSelection;

    if (!counterStratLimitReached) {
      dispatch({ type: actionType, payload: counterstrat });
    } else {
      alert(`You can select a maximum of ${maxSelection} counterstrats.`); // Feedback for the user when the limit is reached
    }
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
