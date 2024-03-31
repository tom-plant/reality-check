import React from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameDispatch, useGameFunction } from '../../contexts/GameContext'; 
import './Alert.css'; 

const Alert = () => {
  const dispatch = useGameDispatch(); 
  const { setCurrentPhase } = useGameFunction();
  const { t } = useTranslation();

  const handleButtonClick = () => {
    setCurrentPhase('game'); 
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'IDENTIFY_WEAKNESSES' });
  };

  return (
    <div className="game-lesson">
      <h2>Alert</h2>
      <p>This is the part of the game where the Alert happens.</p>
      <button onClick={handleButtonClick}>{t('common.continue')} </button>
    </div>
  );
};

export default Alert;
