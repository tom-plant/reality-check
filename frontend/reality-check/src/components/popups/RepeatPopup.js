// RepeatPopup.js

import React from 'react';
import { useGameDispatch } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import './RepeatPopup.css';

const RepeatPopup = ({ onClose }) => {
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_REPEAT_POPUP' });
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_FACTS' });
  };

  return (
    <div className="repeat-popup-overlay">
      <div className="repeat-popup-content">
        <h2>{t('repeatPopup.title')}</h2>
        <p>{t('repeatPopup.instructions')}</p>
        <button className="repeat-button" onClick={handleContinue}>
          {t('common.continue')}
        </button>
      </div>
    </div>
  );
};

export default RepeatPopup;
