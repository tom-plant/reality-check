import React, { useState } from 'react';
import { useGameState } from '../../contexts/GameContext'; 
import SelectFacts from '../game/SelectFacts';
import SelectFactsDisplay from '../game/SelectFactsDisplay'; 
import SelectNarratives from '../game/SelectNarratives';
import SelectNarrativesDisplay from '../game/SelectNarrativesDisplay'; 
import NarrativeImpact from '../game/NarrativeImpact';
import NarrativeImpactDisplay from '../game/NarrativeImpactDisplay';
import IntroduceEvent from '../game/IntroduceEvent';
import IntroduceEventDisplay from '../game/IntroduceEventDisplay';
import EventPopup from '../popups/EventPopup';
import IdentifyWeaknesses from '../game/IdentifyWeaknesses';
import IdentifyWeaknessesDisplay from '../game/IdentifyWeaknessesDisplay';
import UpdatedNarrativeImpact from '../game/UpdatedNarrativeImpact';
import UpdatedNarrativeImpactDisplay from '../game/UpdatedNarrativeImpactDisplay';
import LeftContainer from '../containers/LeftContainer';
import RightContainer from '../containers/RightContainer';
import './GameLayout.css'; // Import CSS

const GameLayout = () => {
  const { currentView, eventOptions } = useGameState();
  const [isEventPopupVisible, setIsEventPopupVisible] = useState(true); // Assuming the popup should be visible initially

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
      case 'UPDATED_NARRATIVE_IMPACT':
        return <UpdatedNarrativeImpact />;
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
        return <NarrativeImpactDisplay />;
      case 'INTRODUCE_EVENT':
        return <IntroduceEventDisplay />;
      case 'IDENTIFY_WEAKNESSES':
        return <IdentifyWeaknessesDisplay />;
      case 'UPDATED_NARRATIVE_IMPACT':
        return <UpdatedNarrativeImpactDisplay />;
      default:
        return <div>Game information or instructions.</div>;
    }
  };

  const closePopup = () => {
    setIsEventPopupVisible(false); // This will close the popup
  };

  return (
    <div className="game-layout">
      <LeftContainer>{renderLeftContent()}</LeftContainer>
      <RightContainer>{renderRightContent()}</RightContainer>
      {currentView === 'INTRODUCE_EVENT' && isEventPopupVisible && (
        <EventPopup events={eventOptions} onClose={closePopup} />
        )}
    </div>
  );
};

export default GameLayout;