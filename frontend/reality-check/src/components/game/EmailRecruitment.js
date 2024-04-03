import React from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next'; 
import messageBackground from '../../assets/gmail_message.png';
import './EmailRecruitment.css'; 


const EmailRecruitment = ({ setCurrentPhase }) => {
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  // Hardcoded email object
  const email = {
    subject: "URGENT Participation Request: Crisis Simulation",
    sender: "The Civic Resilience Project",
    address: "<engage@civicresilience.org>",
    time: "9:17 AM (0 minutes ago)", 
  };

  const handleStart = () => {
    setCurrentPhase('game')
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_FACTS' });
    dispatch({ type: 'TOGGLE_INTRO_POPUP' }); 
  };

  return (
    <div className="email-recruitment" style={{ backgroundImage: `url(${messageBackground})` }}>
      <div className="title-container">
        <p>{email.subject}</p>
      </div>
      <div className="message-container">
        <span className="sender-name">{email.sender}</span>
        <span className="sender-address">{email.address}</span>
        <span className="email-time">{email.time}</span>
      </div>
      <div className="body-container">
        <p>{t('emailRecruitment.intro')}</p>
        <p>{t('emailRecruitment.request')}</p>
        <button onClick={handleStart} style={{ fontWeight: 'bold' }}>
          {t('common.clickToJoin')} 
        </button>
        <p>{t('emailRecruitment.information')}</p>
        <p>{t('emailRecruitment.sendOff')}</p>
        <p>{t('emailRecruitment.goodbye')}</p>
        <p style={{ fontWeight: 'bold' }}>{t('emailRecruitment.sender')}</p>
        <p style={{ fontStyle: 'italic' }}>{t('emailRecruitment.footer')}</p>
      </div>
    </div>
  );
};

export default EmailRecruitment;