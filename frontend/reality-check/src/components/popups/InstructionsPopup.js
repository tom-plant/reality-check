// InstructionsPopup.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import './InstructionsPopup.css'; 

const InstructionsPopup = ({ onClose }) => {
  const { t } = useTranslation();

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <button className="close-btn" onClick={onClose}>X</button>
        <h2>Instructions</h2>
        <p>How to play the game...</p>
      </div>
    </div>
  );
};

export default InstructionsPopup;
