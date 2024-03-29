import React, { useEffect } from 'react';
import i18n from '../../i18n.js'
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
      <p>This is the Email Recruitment screen of the Intro phase. Here, players will be officially recruited and briefed for their mission.</p>
      <button onClick={handleStart}>
        {t('common.start')} 
      </button>
    </div>
  );
};

export default EmailRecruitment;