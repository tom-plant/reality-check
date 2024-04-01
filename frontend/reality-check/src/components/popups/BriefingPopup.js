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
        <h3>{t('introPopup.briefing.keyPointsTitle')}</h3>
        <h4>{t('introPopup.briefing.natureOfCrisis.title')}</h4>
        <p>{t('introPopup.briefing.natureOfCrisis.description')}</p>
        <h4>{t('introPopup.briefing.affectedAreas.title')}</h4>
        <p>{t('introPopup.briefing.affectedAreas.description')}</p>
        <h4>{t('introPopup.briefing.responseMeasures.title')}</h4>
        <p>{t('introPopup.briefing.responseMeasures.description')}</p>
        <h4>{t('introPopup.briefing.challengesAndUnknowns.title')}</h4>
        <p>{t('introPopup.briefing.challengesAndUnknowns.description')}</p>
        <p>{t('introPopup.briefing.conclusion')}</p>
        <p>{t('introPopup.briefing.reminder')}</p>
        <button className="close-btn" onClick={onClose}>X</button>
      </div>
    </div>
  );
};

export default BriefingPopup;
