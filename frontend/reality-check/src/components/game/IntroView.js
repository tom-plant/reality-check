// IntroView.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext';  
import IntroLayout from '../layout/IntroLayout';  

const IntroView = () => {
  const { currentPhase } = useGameState();

  return (
    <div className="intro-view">
      {currentPhase === 'intro' && <IntroLayout />}
    </div>
  );
};

export default IntroView;
