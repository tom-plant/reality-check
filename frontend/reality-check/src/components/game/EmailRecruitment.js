import React from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next'; 
import './EmailRecruitment.css'; 


const EmailRecruitment = ({ setCurrentPhase }) => {
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  const handleStart = () => {
    setCurrentPhase('game')
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_FACTS' });
    dispatch({ type: 'TOGGLE_INTRO_POPUP' }); 
  };

  return (
    <div className="email-recruitment">
      <h2>Email Recruitment</h2>
      <button onClick={handleStart}>
        {t('common.start')} 
      </button>
    </div>
  );
};

export default EmailRecruitment;