import React from 'react';
import { useGameState } from '../../contexts/GameContext'; // Adjust the path as needed
import SelectFacts from '../game/SelectFacts';
import SelectNarratives from '../game/SelectNarratives';
import NarrativeImpact from '../game/NarrativeImpact';
import IntroduceEvent from '../game/IntroduceEvent';
import IdentifyWeaknesses from '../game/IdentifyWeaknesses';
import LeftContainer from '../containers/LeftContainer';
import RightContainer from '../containers/RightContainer';

const GameLayout = () => {
  const { currentView } = useGameState(); // Use the context to get the current view

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
        return <div>Instructions for selecting facts</div>;
      case 'SELECT_NARRATIVES':
        return <div>Guidelines for selecting narratives</div>;
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


  // Example usage
  // goToNextPhase(SELECT_NARRATIVES);