// UpdatedNarrativeImpactDisplay.js

import React, { useState } from 'react';
import { useGameState, useGameFunction, useGameDispatch } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next'; 
import './UpdatedNarrativeImpactDisplay.css'; 

const UpdatedNarrativeImpactDisplay = () => {
  const { selectedNarrative, secondaryNarrative, updatedFactCombination, isLoadingNews } = useGameState();
  const { setCurrentPhase, fetchAndSetConclusion } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 
  const { t } = useTranslation();

  // Progress to outro phase of the game
  const handleContinue = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      fetchAndSetConclusion(); 
      console.log('called fetch and set conclusion')
      setCurrentPhase('outro'); 
      dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'CONCLUSION_WRAP_UP' });
  }};
    
  return (
    <div className="updated-narrative-impact-display-container">
      <div className="updated-narrative-impact-display">
        <h2>{t('common.updatedNarrative')} </h2>
          {secondaryNarrative && (
          <div className="secondary-narrative">
            <p>{secondaryNarrative.text}</p>
          </div>
        )}
        <h2>{t('common.originalNarrative')} </h2>
        {selectedNarrative && (
        <div className="selected-narrative">
          <p>{selectedNarrative.text}</p>
        </div>
      )}
        <h2>{t('common.updatedFacts')} </h2>
        <div className="facts-list">
          {updatedFactCombination.map((fact) => (
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

export default UpdatedNarrativeImpactDisplay;
