import React from 'react';
import { useGameDispatch, useGameFunction } from '../../contexts/GameContext'; 
import './Alert.css'; 

const Alert = () => {
  const dispatch = useGameDispatch(); 
  const { setCurrentPhase } = useGameFunction();

  const handleButtonClick = () => {
    setCurrentPhase('game'); 
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'IDENTIFY_WEAKNESSES' });
  };

  return (
    <div className="game-lesson">
      <h2>Alert</h2>
      <p>This is the part of the game where the Alert happens.</p>
      <button onClick={handleButtonClick}>Continue Game</button>
    </div>
  );
};

export default Alert;
