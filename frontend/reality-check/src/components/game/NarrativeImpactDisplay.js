// NarrativeImpactDisplay.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import './NarrativeImpactDisplay.css'; 

const NarrativeImpactDisplay = () => {
  const { selectedNarrative, selectedFactCombination, isLoadingNews } = useGameState();
  const { t } = useTranslation();
  const dispatch = useGameDispatch();

  // Progress to next game phase
  const handleContinue = () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'INTRODUCE_EVENT' });
  };

    
  return (
    <div className="narrative-impact-display-container">
      <div className="narrative-impact-display">
        <h2>{t('common.yourNarrative')} </h2>
        {selectedNarrative && (
        <div className="selected-narrative">
          <p>{selectedNarrative.text}</p>
        </div>
      )}
        <h2>{t('common.yourFacts')} </h2>
        <div className="facts-list">
          {selectedFactCombination.map((fact) => (
            <div key={fact.id} className="displayed-fact">
              {fact.text}
            </div>
          ))}
        </div>
      </div>
      <button
        className="continue-button"
        onClick={handleContinue}
        disabled={isLoadingNews} 
      >
        {t('common.continue')} 
      </button>
    </div>
  );
};

export default NarrativeImpactDisplay;
