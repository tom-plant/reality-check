import React from 'react';
import { useGameState, useGameFunction } from '../../contexts/GameContext';
import ConclusionWrapUp from '../game/ConclusionWrapUp';
import GameLesson from '../game/GameLesson';
import CenterContainer from '../containers/CenterContainer';
import './OutroLayout.css'; 

const OutroLayout = () => {
  const { currentOutroView } = useGameState();
  const { setCurrentOutroView, setCurrentPhase } = useGameFunction();

  const renderOutroContent = () => {
    switch (currentOutroView) {
      case 'CONCLUSION_WRAP_UP':
        return <ConclusionWrapUp setCurrentOutroView={setCurrentOutroView} />;
      case 'GAME_LESSON':
        return <GameLesson setCurrentPhase={setCurrentPhase}/>;
      default:
        return <ConclusionWrapUp setCurrentOutroView={setCurrentOutroView} />; 
    }
  };

  return (
    <div className="outro-layout">
      <CenterContainer>{renderOutroContent()}</CenterContainer>
    </div>
  );
};

export default OutroLayout;
