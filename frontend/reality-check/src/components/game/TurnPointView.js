// TurnPointView.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext'; 
import TurnPointLayout from '../layout/TurnPointLayout';

const TurnPointView = () => {
  const { currentPhase } = useGameState();

  return (
    <div className="turn-point-view">
      {currentPhase === 'turn-point' && <TurnPointLayout />}
    </div>
  );
};

export default TurnPointView;
