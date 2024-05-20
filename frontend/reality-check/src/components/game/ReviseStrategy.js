import React, { useState } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import StratBox from '../common/StratBox';
import CounterStratBox from '../common/CounterStratBox';
import PublicSentimentGauge from '../common/PublicSentimentGauge';
import './ReviseStrategy.css';

const ReviseStrategy = ({ setCurrentOutroView }) => {
  const { selectedNarrative, selectedCounterNarrative } = useGameState();
  const { setCounterStrategy } = useGameFunction();
  const dispatch = useGameDispatch();
  const { t } = useTranslation();
  const [selectedCounterStrat, setSelectedCounterStrat] = useState(selectedCounterNarrative);

  const handleCounterStratChange = (counterstrat) => {
    setSelectedCounterStrat(counterstrat);
  };

  const handleProceed = () => {
    dispatch({ type: 'SET_SELECTED_COUNTERNARRATIVE', payload: selectedCounterStrat });
    setCounterStrategy(selectedCounterStrat);
    setCurrentOutroView('CONCLUSION_WRAP_UP');
  };

  return (
    <div className="revise-strategies">
      <h2>{t('ReviseStrategy.title')}</h2>
      <div className="strategies-section">
        <h3>{t('ReviseStrategy.originalStrategy')}</h3>
        <StratBox strat={selectedNarrative.strategy} isSelected={true} locked={true} />
      </div>
      <div className="counter-strategies-section">
        <h3>{t('ReviseStrategy.counterStrategy')}</h3>
        {selectedNarrative.counterStrategies.map((counterstrat) => (
          <CounterStratBox
            key={counterstrat.id}
            counterstrat={counterstrat}
            isSelected={selectedCounterStrat === counterstrat}
            onSelect={handleCounterStratChange}
          />
        ))}
      </div>
      <PublicSentimentGauge strategy={selectedCounterStrat} />
      <p>{selectedCounterStrat.effectivenessExplanation}</p>
      <button onClick={handleProceed}>{t('common.proceed')}</button>
    </div>
  );
};

export default ReviseStrategy;
