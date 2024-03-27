// OutroView.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext'; 
import OutroLayout from '../layout/OutroLayout';

const OutroView = () => {
  const { currentPhase } = useGameState();

  return (
    <div className="outro-view">
      {currentPhase === 'outro' && <OutroLayout />}
    </div>
  );
};

export default OutroView;
