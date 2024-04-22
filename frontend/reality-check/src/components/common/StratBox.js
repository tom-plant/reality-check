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



  //   // Check if we are trying to add or remove a strat
  //   const actionType = isSelected ? 'DESELECT_STRAT' : 'SELECT_STRAT';
  //   // Check if adding a strat exceeds the limit of 2
  //   const stratLimitReached = !isSelected && selectedStrat.length >= 2;
  //   console.log(selectedStrat)

  //   if (!stratLimitReached) {
  //     dispatch({ type: actionType, payload: strat });
  //   } else {
  //     alert("You can select a maximum of 2 strategies."); // Feedback for the user when the limit is reached
  //   }
  // };

  // // Check if strat is defined before rendering
  // if (!strat) {
  //   console.error('StratBox received an undefined strat object.');
  //   return null; // Or render some fallback UI
  // }

  // // Determine if the StratBox should be disabled based on selection limit
  // const isDisabled = !isSelected && selectedStrat.length >= 2;

  // return (
  //   <div 
  //     className={`strat-box ${isSelected ? 'selected' : ''} ${isDisabled ? 'disabled' : ''}`}
  //     onClick={toggleStratSelection}
  //   >
  //     {strat.text}
  //   </div>
  // );


export default StratBox;

