// Game.js

import React from 'react';
import { useGameState } from '../contexts/GameContext'; 
import IntroView from '../components/game/IntroView'; 
import GameView from '../components/game/GameView'; 
import TurnPointView from '../components/game/TurnPointView';
import OutroView from '../components/game/OutroView';
import Header from '../components/Header/Header'; 
import DynamicBackground from '../components/DynamicBackground/DynamicBackground';

const Game = () => {
  const { currentPhase } = useGameState();

  const renderPhase = () => {
    switch (currentPhase) {
      case 'intro':
        return <IntroView />;
      case 'game':
        return <GameView />;
      case 'turn-point':
        return <TurnPointView />;
      case 'outro':
        return <OutroView />;
      default:
        return <IntroView />; // Default to IntroView if currentPhase is not set
    }
  };


return (
  <div className="game">
    {currentPhase !== 'intro' && currentPhase !== 'outro' && currentPhase !== 'turn-point' && <Header />}
    <DynamicBackground />
    {renderPhase()}
  </div>
);
};


export default Game;
