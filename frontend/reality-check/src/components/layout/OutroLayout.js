import React from 'react';
import { useGameState, useGameFunction, useGameDispatch } from '../../contexts/GameContext';
import ConclusionWrapUp from '../game/ConclusionWrapUp';
import GameLesson from '../game/GameLesson';
import CenterContainer from '../containers/CenterContainer';
import ReviseStrategy from '../game/ReviseStrategy';
import MatchStrats from '../game/MatchStrats';
import RevisePopup from '../popups/RevisePopup';
import OutroPopup from '../popups/OutroPopup';
import './OutroLayout.css'; 

const OutroLayout = () => {
  const { currentOutroView, isRevisePopupVisible, isOutroPopupVisible } = useGameState();
  const { setCurrentOutroView, setCurrentPhase } = useGameFunction();
  const dispatch = useGameDispatch();

  const renderOutroContent = () => {
    switch (currentOutroView) {
      case 'CONCLUSION_WRAP_UP':
        return <ConclusionWrapUp setCurrentOutroView={setCurrentOutroView} />;
      case 'REVISE_STRATEGY':
        return <ReviseStrategy />;
      case 'MATCH_STRATS':
        return <MatchStrats />;
      case 'GAME_LESSON':
        return <GameLesson setCurrentPhase={setCurrentPhase}/>;
      default:
        return <ConclusionWrapUp setCurrentOutroView={setCurrentOutroView} />; 
    }
  };

  const closeRevisePopup = () => {
    dispatch({ type: 'TOGGLE_REVISE_POPUP' });
  };

  const closeOutroPopup = () => {
    dispatch({ type: 'TOGGLE_OUTRO_POPUP' });
  };

  return (
    <div className="outro-layout">
      <CenterContainer>{renderOutroContent()}</CenterContainer>
      {isRevisePopupVisible && (
        <RevisePopup onClose={closeRevisePopup} />
        )}
      {isOutroPopupVisible && (
        <OutroPopup onClose={closeOutroPopup} />
      )}
    </div>
  );
};

export default OutroLayout;
