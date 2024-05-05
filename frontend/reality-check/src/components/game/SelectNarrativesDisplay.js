// SelectNarrativesDisplay.js
import { useTranslation } from 'react-i18next'; 
import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import './SelectNarrativesDisplay.css'; 

const SelectNarrativesDisplay = () => {
  const { selectedFactCombination } = useGameState();
  const { t } = useTranslation();

  return (
    <div className="select-narratives-display">
      <h2>{t('common.selectedFacts')}</h2>
      <div className="displayed-facts-list">
        {selectedFactCombination.map((fact) => (
          <div key={fact.id} className="displayed-fact">
            {fact.text}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SelectNarrativesDisplay;
