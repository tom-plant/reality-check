// IntroduceEventDisplay.js

import React from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import './IntroduceEventDisplay.css'; 

const IntroduceEventDisplay = () => {
  const { selectedEvent, selectedNarrative, selectedFactCombination, isLoadingNews, introduceEventVisits, inCoda } = useGameState();
  const { setCurrentPhase } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  console.log(inCoda)
  console.log(introduceEventVisits)

  // Progress to next game phase
  const handleContinue = () => {
    // Increment the visit count each time this function is called

    if (introduceEventVisits === 0) {
      // First visit to this phase
      dispatch({ type: 'INCREMENT_INTRODUCE_EVENT_VISITS' });
      dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_FACTS' });
    } else if (introduceEventVisits === 1 && !inCoda) {
      // Second visit, entering coda
      dispatch({ type: 'ENTER_CODA' });
      setCurrentPhase('turn-point'); 
      dispatch({ type: 'SET_CURRENT_TURN_POINT_VIEW', payload: 'ALERT' });
    } else {
      // Subsequent visits or errors could be handled here
      console.error("Unexpected number of visits or state");
    }
  };

  return (
    <div className="introduce-event-display-container">
      <div className="introduce-event-display">
        <h2>{t('common.yourEvent')} </h2>
        {selectedEvent && (
          <div className="selected-event">
            <p>{selectedEvent.text}</p>
          </div>
        )}
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
      <button className="continue-button" onClick={handleContinue} disabled={isLoadingNews}>
      {t('common.continue')} 
      </button>
    </div>
  );
};

export default IntroduceEventDisplay;
