// GameLayout.js
import React from 'react';
import { useGameState } from '../../contexts/GameContext'; // Assuming the correct relative path
import SelectFacts from '../game/SelectFacts';
import SelectNarratives from '../game/SelectNarratives';
import NarrativeImpact from '../game/NarrativeImpact';
import IntroduceEvent from '../game/IntroduceEvent';
import IdentifyWeaknesses from '../game/IdentifyWeaknesses';
import LeftContainer from '../containers/LeftContainer';
import RightContainer from '../containers/RightContainer';

const GameLayout = () => {
    const gameState = useGameState(); // Use the hook directly to access the game state

  const renderGamePhase = () => {
    switch(gameState.currentView) { // Use gameState.currentView to determine the phase
      case 'SELECT_FACTS':
        return <SelectFacts />;
      case 'SELECT_NARRATIVES':
        return <SelectNarratives />;
      case 'NARRATIVE_IMPACT':
        return <NarrativeImpact />;
      case 'INTRODUCE_EVENT':
        return <IntroduceEvent />;
      case 'IDENTIFY_WEAKNESSES':
        return <IdentifyWeaknesses />;
      default:
        return <SelectFacts />; // Default to SelectFacts or any other default view you prefer
    }
  };

  return (
    <div className="game-layout">
      <LeftContainer>
        {renderGamePhase()}
      </LeftContainer>
      <RightContainer>
        {/* Content for the right container, potentially based on the game phase */}
      </RightContainer>
    </div>
  );
};

export default GameLayout;
