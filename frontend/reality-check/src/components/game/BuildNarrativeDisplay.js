import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import StratBox from '../StratBox/StratBox'; 
import './BuildNarrativeDisplay.css'; 

const BuildNarrativeDisplay = () => {
  const { t } = useTranslation();
  const { strats } = useGameState();
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 

// Generate narratives and change view, assuring button can only be clicked once
const handleGenerateNarrative = async () => {
    if (!buttonClicked) { 
        setButtonClicked(true); 
        dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_NARRATIVES' });
        await buildAndSetNarrative(selectedFactCombination);
    }
    };
    
  return (
    <div className="build-narratives">
      <h2>{t('buildNarratives.title')}</h2>
      <div className="strats-list">
        {strats.map((strat) => (
          <StratBox
            key={strat.id}
            actor={strat.text}
            isSelected={strat === selectedStrat} //idk about this line
          />
        ))}
      </div>
      <button className="generate-narrative" 
        onClick={handleGenerateNarrative}>
        {t('common.confirmSelections')} 
      </button>
    </div>
  );
};

export default BuildNarrativeDisplay;