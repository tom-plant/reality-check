// InstructionsPopup.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import './InstructionsPopup.css'; 

const InstructionsPopup = ({ onClose }) => {
  const { t } = useTranslation();

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>{t('introPopup.instructions.title')}</h2>
        <p>{t('introPopup.instructions.introduction')}</p>
        <h3>{t('introPopup.instructions.whatYouWillDoTitle')}</h3>
        <p>{t('introPopup.instructions.engageScenarios')}</p>
        <p>{t('introPopup.instructions.informedDecisionMaking')}</p>
        <p>{t('introPopup.instructions.criticalAnalysis')}</p>
        <p>{t('introPopup.instructions.conclusion')}</p>
        <p>{t('introPopup.instructions.readyToBegin')}</p>
        <button className="close-btn" onClick={onClose}>X</button>
      </div>
    </div>
  );
};

export default InstructionsPopup;
