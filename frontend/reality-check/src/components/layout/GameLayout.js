import React from 'react';
import { useGameState } from '../../contexts/GameContext'; 
import SelectFacts from '../game/SelectFacts';
import SelectFactsDisplay from '../game/SelectFactsDisplay'; 
import SelectNarratives from '../game/SelectNarratives';
import SelectNarrativesDisplay from '../game/SelectNarrativesDisplay'; 
import NarrativeImpact from '../game/NarrativeImpact';
import IntroduceEvent from '../game/IntroduceEvent';
import IdentifyWeaknesses from '../game/IdentifyWeaknesses';
import LeftContainer from '../containers/LeftContainer';
import RightContainer from '../containers/RightContainer';
import './GameLayout.css'; // Import CSS

const GameLayout = () => {
  const { currentView } = useGameState();

  // Use currentView to determine the content for LeftContainer and RightContainer
  // Implement renderLeftContent and renderRightContent functions as shown previously

  const renderLeftContent = () => {
    switch (currentView) { // Switch based on currentView from context
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
        return <div>Welcome to the game! Please select an option to start.</div>;
    }
  };

  const renderRightContent = () => {
    // Example implementations. Adjust according to your game design.
    switch (currentView) {
      case 'SELECT_FACTS':
        return <SelectFactsDisplay />;
      case 'SELECT_NARRATIVES':
        return <SelectNarrativesDisplay />;
      case 'NARRATIVE_IMPACT':
        return <div>Impact of your narrative choices</div>;
      case 'INTRODUCE_EVENT':
        return <div>Details of the new event</div>;
      case 'IDENTIFY_WEAKNESSES':
        return <div>Identify weaknesses in the narrative</div>;
      default:
        return <div>Game information or instructions.</div>;
    }
  };

  return (
    <div className="game-layout">
      <LeftContainer>{renderLeftContent()}</LeftContainer>
      <RightContainer>{renderRightContent()}</RightContainer>
    </div>
  );
};

export default GameLayout;