// InstructionsPopup.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import { FaTimesCircle } from 'react-icons/fa';  // Importing a times icon from react-icons
import './InstructionsPopup.css'; 

const InstructionsPopup = ({ onClose }) => {
  const { t } = useTranslation();

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>{t('introPopup.instructions.title')}</h2>
        <p>{t('introPopup.instructions.introduction')}</p>
        <h3>{t('introPopup.instructions.whatYouWillDoTitle')}</h3>
        <div className="left-aligned-container">
          <p>{t('introPopup.instructions.engageScenarios')}</p>
          <p>{t('introPopup.instructions.informedDecisionMaking')}</p>
          <p>{t('introPopup.instructions.criticalAnalysis')}</p>
          <p>{t('introPopup.instructions.changeOutcome')}</p>
        </div>
        <p>{t('introPopup.instructions.conclusion')}</p>
        <button className="close-button" onClick={onClose}>
          <FaTimesCircle />  
        </button>
      </div>
    </div>
  );
};


export default InstructionsPopup;
