//GameView.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext'; 
import GameLayout from '../layout/GameLayout'; 

const GameView = () => {
  const { currentPhase } = useGameState();

  return (
    <div className="game-view">
      {currentPhase === 'game' && <GameLayout />}
    </div>
  );
};

export default GameView;