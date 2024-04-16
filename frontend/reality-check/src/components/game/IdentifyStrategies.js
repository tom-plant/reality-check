import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import CounterStratBox from '../CounterStratBox/CounterStratBox'; 
import './IdentifyStrategies.css'; 

const IdentifyStrategies = () => {
  const { t } = useTranslation();
  const { counterstrats } = useGameState();

  // Progress to next game phase
  const handleContinue = () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'UPDATED_NARRATIVE_IMPACT' });
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
      <button className="continue-button" onClick={handleContinue} disabled={isLoadingNews}>
      {t('common.continue')} 
      </button>
    </div>
  );
};

export default IdentifyStrategies;
