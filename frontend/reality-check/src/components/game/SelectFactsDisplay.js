// SelectFactsDisplay.js

import React, { useState } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next'; 
import FactBox from '../common/FactBox'; 
import './SelectFactsDisplay.css';

const SelectFactsDisplay = () => {
  const { selectedFactCombination, timerHasEnded } = useGameState();
  const { fetchAndSetNarratives } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 
  const { t } = useTranslation();

  // Generate narratives and change view, assuring button can only be clicked once
  const handleGenerateNarrative = async () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_NARRATIVES' });
      await fetchAndSetNarratives(selectedFactCombination);
      dispatch({ type: 'COPY_FACTS_TO_UPDATED', payload: selectedFactCombination }); 
      dispatch({ type: 'RESET_SELECTION_ENDED' });
    }
  };

  return (
    <div className="select-facts-display">
      <div className="spacer"></div>
      <div className="facts-list">
        {selectedFactCombination.map((fact) => (
          <FactBox 
            key={fact.id}
            fact={fact}
            isSelected={true} 
            disabled={timerHasEnded} 
            container="right"
          />
        ))}
      </div>
      <button className="generate-narrative" 
        disabled={!timerHasEnded}
        onClick={handleGenerateNarrative}>
        {t('common.generateNarrative')} 
      </button>
    </div>
  );
};


export default SelectFactsDisplay;






