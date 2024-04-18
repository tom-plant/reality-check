import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import StratBox from '../common/StratBox'; 
import './BuildNarrativeDisplay.css'; 

const BuildNarrativeDisplay = () => {
  const { t } = useTranslation();
  const { buildAndSetNarrative } = useGameFunction();
  const { strats, selectedStrat, selectedActor } = useGameState();
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 

// Generate narratives and change view, assuring button can only be clicked once
const handleGenerateNarrative = async () => {
    if (!buttonClicked) { 
        setButtonClicked(true); 
        dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_NARRATIVES' });
        await buildAndSetNarrative(selectedActor, selectedStrat); 
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
            isSelected={strat === selectedStrat} 
            disabled={selectedStrat.length >= 2 && !selectedStrat.includes(strat)}
          />
        ))}
      </div>
      <button className="generate-narrative" 
        onClick={handleGenerateNarrative}
        disabled={selectedStrat.length < 2 || !selectedActor}
      >
        {t('common.confirmSelections')} 
      </button>
    </div>
  );
};

export default BuildNarrativeDisplay;