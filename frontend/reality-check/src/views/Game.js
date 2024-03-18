// Game.js

import React, { useState } from 'react';
import { useEffect } from 'react';
import Header from '../components/Header/Header'; 
import DynamicBackground from '../components/DynamicBackground/DynamicBackground';
import GameLayout from '../components/layout/GameLayout'; 
import './Game.css'; 

const Game = () => {

  // State to manage the current game phase, e.g., 'intro', 'game', 'outro'
  const [currentPhase, setCurrentPhase] = useState('game'); // Defaulting to 'game' for now

  // Render function to determine what to display based on the current game phase
  const renderGamePhase = () => {
    switch (currentPhase) {
      case 'intro':
        // return <IntroView />;
        break; // Placeholder for IntroView component
      case 'game':
        return <GameLayout />; // Rendering GameLayout as the main game view
      case 'outro':
        // return <OutroView />;
        break; // Placeholder for OutroView component
      default:
        return <GameLayout />; // Default to GameLayout for now
    }
  };


return (
  <div className="game">
    <Header />
    <div className="line line-1"></div>
    <div className="line line-2"></div>
    <div className="line line-3"></div>
    <div className="line line-4"></div>
    <div className="line line-5"></div>
    <DynamicBackground />
    {renderGamePhase()} {/* Call the function to render based on the current phase */}
  </div>
);
};



export default Game;
