// IdentifyStrategiesDisplay.js

import { useTranslation } from 'react-i18next'; 
import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import './IdentifyStrategiesDisplay.css'; 

const IdentifyStrategiesDisplay = () => {
  const { selectedNarrative, updatedFactCombination, selectedStrat } = useGameState();
  const { t } = useTranslation();

return (
  <div className="identify-strategies-display-container">
    <div className="identify-strategies-display">
      <h2>{t('common.yourNarrative')} </h2>
      {selectedNarrative && (
        <div className="selected-narrative">
          <p>{selectedNarrative.text}</p>
        </div>
      )}
      <h2>{t('common.yourStrategy')} </h2>
      {selectedStrat && (
        <div className="selected-narrative">
          <p>{selectedStrat.text}</p>
        </div>
      )}
      <h2>{t('common.yourUpdatedFacts')} </h2>
      <div className="selected-facts-list">
        {updatedFactCombination.map((fact) => (
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

