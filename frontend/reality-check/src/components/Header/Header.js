//components/Header.js

import React, { useState } from 'react';
import './Header.css';
import BriefingPopup from '../popups/BriefingPopup';
import InstructionsPopup from '../popups/InstructionsPopup';
import ProgressBar from './ProgressBar'

const Header = () => {
  const [showBriefing, setShowBriefing] = useState(false);
  const [showInstructions, setShowInstructions] = useState(false);

  const toggleBriefing = () => setShowBriefing(!showBriefing);
  const toggleInstructions = () => setShowInstructions(!showInstructions);

  return (
    <>
      <div className="header">
        <div className="progress-container">
          <ProgressBar />
        </div>
        <div className="header-items">
          <span className="header-item" onClick={toggleBriefing}>Briefing</span>
          <span className="header-item" onClick={toggleInstructions}>Instructions</span>
        </div>
      </div>
      {showBriefing && <BriefingPopup onClose={toggleBriefing} />}
      {showInstructions && <InstructionsPopup onClose={toggleInstructions} />}
    </>
  );
};



export default Header;
