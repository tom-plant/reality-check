// ProgressBar.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import './ProgressBar.css';

const ProgressBar = () => {
  const { currentPhase, currentView, currentIntroView, currentTurnPointView, currentOutroView, introduceEventVisits, inCoda } = useGameState();
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const calculateProgress = () => {
      let step = 0;

      if (currentPhase === 'intro') {
        switch (currentIntroView) {
          case 'EXPO_INBOX':
            step = 1;
            console.log('expo')
            break;
          case 'EMAIL_RECRUITMENT':
            step = 2;
            console.log('email')
            break;
          default:
            step = 0;
        }
      } else if (currentPhase === 'game') {
        switch (currentView) {
          case 'SELECT_FACTS':
            step = introduceEventVisits === 1 ? 11 : 3;
            console.log('select')
            break;
          case 'BUILD_NARRATIVE':
            step = introduceEventVisits === 1 ? 12 : 4;
            console.log('build')
            break;
          case 'SELECT_NARRATIVES':
            step = introduceEventVisits === 1 ? 13 : 5;
            console.log('event')
            break;
          case 'NARRATIVE_IMPACT':
            step = introduceEventVisits === 1 ? 14 : 6;
            break;
          case 'INTRODUCE_EVENT':
            step = introduceEventVisits === 1 ? 15 : 7;
            break;
          case 'IDENTIFY_WEAKNESSES':
            step = 16;
            break;
          case 'IDENTIFY_STRATEGIES':
            step = 17;
            break;
          case 'UPDATED_NARRATIVE_IMPACT':
            step = 18;
            break;
          default:
            step = 0;
        }
      } else if (currentPhase === 'turn-point' && currentTurnPointView === 'ALERT') {
        step = 8;
      } else if (currentPhase === 'outro') {
        switch (currentOutroView) {
          case 'CONCLUSION_WRAP_UP':
            step = 19;
            break;
          case 'GAME_LESSON':
            step = 20;
            break;
          default:
            step = 0;
        }
      }

      setProgress((step / 20) * 100);
    };

    calculateProgress();
  }, [currentPhase, currentView, currentIntroView, currentTurnPointView, currentOutroView, introduceEventVisits, inCoda]);

  return (
    <div className="progress-bar">
      <div className="progress-bar-fill" style={{ width: `${progress}%` }}></div>
    </div>
  );
};

export default ProgressBar;
