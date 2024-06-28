// Emailpopup.js

import React from 'react';
import { useGameDispatch } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import './EmailPopup.css';

const EmailPopup = ({ onClose }) => {
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_EMAIL_POPUP' });
  };

  return (
    <div className="email-popup-overlay">
      <div className="email-popup-content">
        <h2>{t('emailPopup.title')}</h2>
        <p>{t('emailPopup.instructions')}</p>
        <button className="email-button" onClick={handleContinue}>
          {t('common.continue')}
        </button>
      </div>
    </div>
  );
};

export default EmailPopup;
