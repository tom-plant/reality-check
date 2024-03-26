// Game.js

import React from 'react';
import { useGameState } from '../contexts/GameContext'; // Adjust the import path as needed
import IntroView from '../components/game/IntroView'; // Adjust the import path as needed
import GameView from '../components/game/GameView'; // Adjust the import path as needed
import OutroView from '../components/game/OutroView'; // Adjust the import path as needed
import Header from '../components/Header/Header'; 
import DynamicBackground from '../components/DynamicBackground/DynamicBackground';

const Game = () => {
  const { currentPhase } = useGameState(); // Use the context to get the current phase

  const renderPhase = () => {
    switch (currentPhase) {
      case 'intro':
        return <IntroView />;
      case 'game':
        return <GameView />;
      case 'outro':
        return <OutroView />;
      default:
        return <IntroView />; // Default to IntroView if currentPhase is not set
    }
  };


return (
  <div className="game">
    <Header />
    <DynamicBackground />
    {renderPhase()} {/* Call the function to render based on the current phase */}
  </div>
);
};


export default Game;
