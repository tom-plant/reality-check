//GameView.js

import React from 'react';
import { useGameState, useGameFunction } from '../../contexts/GameContext'; 
import GameLayout from '../layout/GameLayout'; 

const GameView = () => {
  const { setCurrentPhase } = useGameFunction(); 
  const { currentPhase } = useGameState();

  return (
    <div className="game-view">
      {currentPhase === 'game' && <GameLayout />}
    </div>
  );
};

export default GameView;