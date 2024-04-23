// CounterStratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './CounterStratBox.css'; 

const CounterStratBox = ({ counterstrat, isSelected }) => {
  const dispatch = useGameDispatch();
  const { selectedCounterStrat } = useGameState(); // Access the selected facts from context

  const toggleCounterStratSelection = () => {
    let actionType, counterStratLimitReached;

    actionType = isSelected ? 'DESELECT_COUNTERSTRAT' : 'SELECT_COUNTERSTRAT';
    counterStratLimitReached = !isSelected && selectedCounterStrat.length >= 2;

    if (!counterStratLimitReached) {
      dispatch({ type: actionType, payload: counterstrat });
    } else {
      alert("You can select a maximum of 2 counterstrats."); // Feedback for the user when the limit is reached
    }
  };

  return (
    <div 
      className={`counter-strat-box ${isSelected ? 'selected' : ''}`} 
      onClick={toggleCounterStratSelection}
    >
      {counterstrat.text}
    </div>
  );
};

export default CounterStratBox;
