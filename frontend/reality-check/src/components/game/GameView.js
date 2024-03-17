//GameView.js

import React, { useState } from 'react';
import { useGameDispatch } from '../../contexts/GameContext'; // Adjust path as needed
import GameLayout from '../layout/GameLayout'; // Adjust the path as needed

const GameView = () => {
  const dispatch = useGameDispatch();

  // Function to transition to the next phase
  const goToNextPhase = (nextPhase) => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: nextPhase });
  };

  return (
    <div className="game-view">
      <GameLayout goToNextPhase={goToNextPhase} />
    </div>
  );
};

export default GameView;