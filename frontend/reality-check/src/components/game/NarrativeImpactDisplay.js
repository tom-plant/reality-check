// NarrativeImpactDisplay.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import './NarrativeImpactDisplay.css'; 

const NarrativeImpactDisplay = () => {
  const { selectedNarrative, selectedFactCombination, isLoadingNews, inCoda, introduceEventVisits, contentError } = useGameState();
  const { t } = useTranslation();
  const { combineContentAndCommitPrimary } = useGameFunction(); 
  const dispatch = useGameDispatch();

  // Progress to next game phase
  const handleContinue = () => {
    if (introduceEventVisits === 1 && !inCoda) {
      // Second visit, show the event popup and clear the event news content
      combineContentAndCommitPrimary(selectedNarrative);
      dispatch({ type: 'CLEAR_EVENT_NEWS_CONTENT' });
    }
    if (introduceEventVisits === 0 && !inCoda) {
      // First visit only, combine content and commit as primary narrative
      combineContentAndCommitPrimary(selectedNarrative);
      dispatch({ type: 'CLEAR_SOCIAL_MEDIA_CONTENT' });
    }
    dispatch({ type: 'TOGGLE_EVENT_POPUP' });
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
        <div className="displayed-facts-list">
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
        disabled={isLoadingNews || contentError} 
      >
        {t('common.continue')} 
      </button>
    </div>
  );
};

export default NarrativeImpactDisplay;
