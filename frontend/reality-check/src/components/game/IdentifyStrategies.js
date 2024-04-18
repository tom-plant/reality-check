import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import CounterStratBox from '../common/CounterStratBox'; 
import './IdentifyStrategies.css'; 

const IdentifyStrategies = () => {
  const { t } = useTranslation();
  const { counterstrats, updatedFactCombination, selectedCounterStrat } = useGameState();
  const [buttonClicked, setButtonClicked] = useState(false); 
  const dispatch = useGameDispatch();
  const { identifyWeaknessesAndSetContent } = useGameFunction();


  // Progress to next game phase
  const handleContinue = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      dispatch({ type: 'SET_CURRENT_VIEW', payload: 'UPDATED_NARRATIVE_IMPACT' });
      setTimeout(() => {
        identifyWeaknessesAndSetContent(updatedFactCombination, selectedCounterStrat);
      }, 0); 
    }
  };


  return (
    <div className="identify-strategies">
      <h2>{t('identifyStrategies.title')}</h2>
      <div className="counter-strats-list">
        {counterstrats.map((counterstrat) => (
          <CounterStratBox
            key={counterstrat.id}
            counterstrat={counterstrat.text}
            isSelected={counterstrat === selectedCounterStrat} //idk about this line
          />
        ))}
      </div>
      <button className="continue-button" onClick={handleContinue} disabled={!selectedCounterStrat}>
      {t('common.continue')} 
      </button>
    </div>
  );
};

export default IdentifyStrategies;
