// IdentifyStrategiesDisplay.js

import { useTranslation } from 'react-i18next'; 
import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import './SelectNarrativesDisplay.css'; 

const IdentifyStrategiesDisplay = () => {
  const { selectedFactCombination, selectedNarrative } = useGameState();
  const { t } = useTranslation();

return (
  <div className="identify-strategies-display-container">
    <div className="introduce-event-display">
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
  </div>
);
};

export default IdentifyStrategiesDisplay;

