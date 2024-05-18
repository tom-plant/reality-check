import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import StratBox from '../common/StratBox'; 
import Counter from '../common/Counter';
import './BuildNarrativeDisplay.css'; 

const BuildNarrativeDisplay = () => {
  const { strats, selectedStrat, selectedActor, inCoda, introduceEventVisits } = useGameState();
  const { t } = useTranslation();
  const { buildAndSetNarrative } = useGameFunction();
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 
  const [initialSelections, setInitialSelections] = useState({
    actor: null,
    strats: [],
  });

  // Set initial selections on first render
  useEffect(() => {
    if (!initialSelections.actor && !initialSelections.strats.length) {
      setInitialSelections({
        actor: selectedActor,
        strats: selectedStrat,
      });
    }
  }, [selectedActor, selectedStrat, initialSelections]);

  // Generate narratives and change view, assuring button can only be clicked once
  const handleGenerateNarrative = async () => {
    if (!buttonClicked) {
      if (introduceEventVisits === 1 && !inCoda) {
        const actorChanged = initialSelections.actor !== selectedActor;
        const stratsChanged = selectedStrat.some((strat, index) => strat !== initialSelections.strats[index]);
        
        if (!actorChanged && !stratsChanged) {
          alert("You must change your selections before proceeding");
          return;
        }
      }

      setButtonClicked(true); 
      dispatch({ type: 'SET_CURRENT_VIEW', payload: 'SELECT_NARRATIVES' });
      await buildAndSetNarrative(selectedActor, selectedStrat); 
    }
  };
  
    const isButtonEnabled = selectedActor && Array.isArray(selectedStrat) && selectedStrat.length === 2;
    
    return (
      <div className="build-narratives-display">
        <h2>{t('buildNarratives.display')}</h2>
        <div className="strats-list">
          {strats && strats.map((strat) => (
            <StratBox
              key={strat.id}
              strat={strat}
              isSelected={selectedStrat.includes(strat)}
            />
          ))}
        </div>
        <div className="counter-wrapper">
            <Counter />  
        </div> 
        <button className="generate-narrative" 
          onClick={handleGenerateNarrative}
          disabled={!isButtonEnabled}
        >
          {t('common.confirmSelections')} 
        </button>
      </div>
    );
};

export default BuildNarrativeDisplay;