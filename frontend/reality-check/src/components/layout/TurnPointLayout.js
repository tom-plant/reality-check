import React from 'react';
import { useGameState, useGameFunction } from '../../contexts/GameContext';
import CenterContainer from '../containers/CenterContainer';
import Alert from '../game/Alert';
import './TurnPointLayout.css'; 

const TurnPointLayout = () => {
  const { currentTurnPointView } = useGameState();
  const { setCurrentTurnPointView, setCurrentPhase } = useGameFunction();

  const renderTurnPointContent = () => {
    switch (currentTurnPointView) {
      case 'ALERT':
        return <Alert setCurrentTurnPointView={setCurrentTurnPointView} setCurrentPhase={setCurrentPhase} />;
      default:
        return <Alert setCurrentTurnPointView={setCurrentTurnPointView} setCurrentPhase={setCurrentPhase} />;
    }
  };

  return (
    <div className="turn-point-layout">
      <CenterContainer>{renderTurnPointContent()}</CenterContainer>
    </div>
  );
};

export default TurnPointLayout;
