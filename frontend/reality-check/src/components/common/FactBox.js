import React from 'react';
import { useGameDispatch } from '../../contexts/GameContext'; // Adjust the path as needed

const FactBox = ({ fact, isSelected }) => {
  const dispatch = useGameDispatch();

  const toggleFactSelection = () => {
    const actionType = isSelected ? 'DESELECT_FACT' : 'SELECT_FACT';
    dispatch({ type: actionType, payload: fact });
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