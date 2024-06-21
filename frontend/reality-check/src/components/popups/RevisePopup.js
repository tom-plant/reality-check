// RevisePopup.js

import React from 'react';
import { useGameDispatch } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import './RevisePopup.css';

const RevisePopup = ({ onClose }) => {
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_REVISE_POPUP' });
  };

  return (
    <div className="revise-popup-overlay">
      <div className="revise-popup-content">
        <h2>{t('revisePopup.title')}</h2>
        <p>{t('revisePopup.instructions')}</p>
        <button className="revise-button" onClick={handleContinue}>
          {t('common.continue')}
        </button>
      </div>
    </div>
  );
};

export default RevisePopup;
