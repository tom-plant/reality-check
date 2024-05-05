// UpdatedNarrativeImpactDisplay.js

import React, { useState } from 'react';
import { useGameState, useGameFunction, useGameDispatch } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next'; 
import './UpdatedNarrativeImpactDisplay.css'; 

const UpdatedNarrativeImpactDisplay = () => {
  const { selectedNarrative, secondaryNarrative, selectedCounterStrat, updatedFactCombination } = useGameState();
  const { t } = useTranslation();


    
  return (
    <div className="updated-narrative-impact-display-container">
      <div className="updated-narrative-impact-display">
        <h2>{t('common.originalNarrative')}</h2>
        {selectedNarrative && (
          <div className="selected-narrative">
            <p>{selectedNarrative.text}</p>
          </div>
        )}
        <h2>{t('common.updatedFacts')}</h2>
        <div className="displayed-facts-list">
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

export default UpdatedNarrativeImpactDisplay;
