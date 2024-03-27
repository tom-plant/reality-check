import React from 'react';
import { useGameFunction } from '../../contexts/GameContext';  
import IntroLayout from '../layout/IntroLayout';  

const IntroView = () => {
  const { setCurrentPhase } = useGameFunction();

  // Example function to transition to the main game
  const goToMainGame = () => {
    setCurrentPhase('game');
  };

  return (
    <div className="intro-view">
      <IntroLayout />
    </div>
  );
};

export default IntroView;
