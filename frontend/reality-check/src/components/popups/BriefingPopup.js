// BriefingPopup.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import { FaTimesCircle } from 'react-icons/fa';  // Importing a times icon from react-icons
import './BriefingPopup.css'; 


const BriefingPopup = ({ onClose }) => {
  const { t } = useTranslation();

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>{t('introPopup.briefing.title')}</h2>
        <p>{t('introPopup.briefing.introduction')}</p>
        <p>{t('introPopup.briefing.note')}</p>
        <p>{t('introPopup.briefing.natureOfCrisis.description')}</p>
        <p>{t('introPopup.briefing.affectedAreas.description')}</p>
        <p>{t('introPopup.briefing.responseMeasures.description')}</p>
        <p>{t('introPopup.briefing.conclusion')}</p>
          <button className="close-button" onClick={onClose}>
            <FaTimesCircle />  
          </button>
      </div>
    </div>
  );
};

export default BriefingPopup;
