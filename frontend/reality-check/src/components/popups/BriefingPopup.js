// BriefingPopup.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
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
        <button className="close-btn" onClick={onClose}>X</button>
      </div>
    </div>
  );
};

export default BriefingPopup;
