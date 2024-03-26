//GameView.js

import React, { useState } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext'; // Adjust path as needed
import GameLayout from '../layout/GameLayout'; // Adjust the path as needed

const GameView = () => {
  const dispatch = useGameDispatch();
  const { setCurrentPhase } = useGameFunction(); 
  const { currentPhase } = useGameState();

  // Placeholder for transition functions, adjust as needed
  const transitionToEnd = () => {
    setCurrentPhase('outro');
  };

  return (
    <div className="game-view">
      {currentPhase === 'game' && <GameLayout />}
      {/* Handle other phases like 'outro' as needed */}
    </div>
  );
};

export default GameView;