// Outropopup.js

import React from 'react';
import { useGameDispatch } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import './OutroPopup.css';

const OutroPopup = ({ onClose }) => {
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_OUTRO_POPUP' });
  };

  return (
    <div className="outro-popup-overlay">
      <div className="outro-popup-content">
        <h2>{t('outroPopup.title')}</h2>
        <p>{t('outroPopup.instructions')}</p>
        <button className="outro-button" onClick={handleContinue}>
          {t('common.continue')}
        </button>
      </div>
    </div>
  );
};

export default OutroPopup;
