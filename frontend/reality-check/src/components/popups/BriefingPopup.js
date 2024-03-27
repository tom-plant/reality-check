// BriefingPopup.js

import React from 'react';
import './BriefingPopup.css'; 

const BriefingPopup = ({ onClose }) => {
  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <button className="close-btn" onClick={onClose}>X</button>
        <h2>Briefing</h2>
        <p>Here is some important information for players...</p>
      </div>
    </div>
  );
};

export default BriefingPopup;
