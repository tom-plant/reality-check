import React, { useState } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext'; 
import IntroPopup from '../popups/IntroPopup';
import SelectFacts from '../game/SelectFacts';
import SelectFactsDisplay from '../game/SelectFactsDisplay'; 
import BuildNarrative from '../game/BuildNarrative';
import BuildNarrativeDisplay from '../game/BuildNarrativeDisplay';
import SelectNarratives from '../game/SelectNarratives';
import SelectNarrativesDisplay from '../game/SelectNarrativesDisplay'; 
import NarrativeImpact from '../game/NarrativeImpact';
import NarrativeImpactDisplay from '../game/NarrativeImpactDisplay';
import IntroduceEvent from '../game/IntroduceEvent';
import IntroduceEventDisplay from '../game/IntroduceEventDisplay';
import RepeatPopup from '../popups/RepeatPopup'; 
import EventPopup from '../popups/EventPopup';
import IdentifyWeaknesses from '../game/IdentifyWeaknesses';
import IdentifyWeaknessesDisplay from '../game/IdentifyWeaknessesDisplay';
import IdentifyStrategies from '../game/IdentifyStrategies';
import IdentifyStrategiesDisplay from '../game/IdentifyStrategiesDisplay';
import UpdatedNarrativePopup from '../popups/UpdatedNarrativePopup'
import UpdatedNarrativeImpact from '../game/UpdatedNarrativeImpact';
import UpdatedNarrativeImpactDisplay from '../game/UpdatedNarrativeImpactDisplay';
import LeftContainer from '../containers/LeftContainer';
import RightContainer from '../containers/RightContainer';
import GameInstructions from '../containers/GameInstructions'
import './GameLayout.css'; 

const GameLayout = () => {
  const { currentView, isUpdatedNarrativePopupVisible, isEventPopupVisible, isIntroPopupVisible, isRepeatPopupVisible } = useGameState();
  const dispatch = useGameDispatch();

  const renderLeftContent = () => {
    switch (currentView) { 
      case 'SELECT_FACTS':
        return <SelectFacts />;
      case 'BUILD_NARRATIVE':
        return <BuildNarrative />;
      case 'SELECT_NARRATIVES':
        return <SelectNarratives />;
      case 'NARRATIVE_IMPACT':
        return <NarrativeImpact />;
      case 'INTRODUCE_EVENT':
        return <IntroduceEvent />;
      case 'IDENTIFY_WEAKNESSES':
        return <IdentifyWeaknesses />;
      case 'IDENTIFY_STRATEGIES':
        return <IdentifyStrategies />;
      case 'UPDATED_NARRATIVE_IMPACT':
        return <UpdatedNarrativeImpact />;
      default:
        return <div>Uh oh... something went wrong.</div>;
    }
  };

  const renderRightContent = () => {
    switch (currentView) {
      case 'SELECT_FACTS':
        return <SelectFactsDisplay />;
      case 'BUILD_NARRATIVE':
        return <BuildNarrativeDisplay />;
      case 'SELECT_NARRATIVES':
        return <SelectNarrativesDisplay />;
      case 'NARRATIVE_IMPACT':
        return <NarrativeImpactDisplay />;
      case 'INTRODUCE_EVENT':
        return <IntroduceEventDisplay />;
      case 'IDENTIFY_WEAKNESSES':
        return <IdentifyWeaknessesDisplay />;
      case 'IDENTIFY_STRATEGIES':
        return <IdentifyStrategiesDisplay />;
      case 'UPDATED_NARRATIVE_IMPACT':
        return <UpdatedNarrativeImpactDisplay />;
      default:
        return <div>Uh oh... something went wrong.</div>;
    }
  };

  const closeEventPopup = () => {
    dispatch({ type: 'TOGGLE_EVENT_POPUP' });
  };

  const closeUpdatedNarrativePopup = () => {
    dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' });
  };

  const closeIntroPopup = () => {
    dispatch({ type: 'TOGGLE_INTRO_POPUP' });
  };

  return (
    <div className="game-layout">
      <GameInstructions />
      <LeftContainer>{renderLeftContent()}</LeftContainer>
      <RightContainer>{renderRightContent()}</RightContainer>
      {isEventPopupVisible && (
        <EventPopup onClose={closeEventPopup} />
        )}
      {isUpdatedNarrativePopupVisible && (
        <UpdatedNarrativePopup onClose={closeUpdatedNarrativePopup} />
      )}
      {isIntroPopupVisible && (
        <IntroPopup onClose={closeIntroPopup} />
      )}
      {isRepeatPopupVisible && (
        <RepeatPopup onClose={() => dispatch({ type: 'TOGGLE_REPEAT_POPUP' })} />
      )}
    </div>
  );
};

export default GameLayout;