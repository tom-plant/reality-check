//ConclusionWrapUp.js
import React, { useState, useEffect } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import LoadingIcon from '../common/LoadingIcon'; 
import StratBox from '../common/StratBox'; 
import CounterStratBox from '../common/CounterStratBox';
import NarrativeBox from '../common/NarrativeBox';
import './ConclusionWrapUp.css';

const ConclusionWrapUp = () => {
  const { conclusionContent, isLoadingConclusion, selectedNarrative, selectedCounterNarrative } = useGameState();
  const { t } = useTranslation();
  const [buttonClicked, setButtonClicked] = useState(false); 
  const dispatch = useGameDispatch();

  // Handle retry or choose a weaker strategy
  const handleButtonClick = () => {
    setButtonClicked(false);
    dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'REVISE_STRATEGY' });
  };

  // Format strategies to objects with text property
  const formattedSelectedStrat = { text: selectedNarrative.strategy };
  const formattedSelectedCounterStrat = { text: selectedCounterNarrative.strategy };

  const getOutcomeText = (effectiveness) => {
    if (!effectiveness) {
      return 'Loading';
    }

    switch (effectiveness.toLowerCase()) {
      case 'strong':
        return 'Peace';
      case 'medium':
        return 'Resolution';
      case 'weak':
        return 'Chaos';
      default:
        return 'Loading';
    }
  };

  return (
    <div className="conclusion-wrap-up">
      <div className="left-section">
        <h2>Did you preserve the peace?</h2>
        <div className="outcome-box">
          <span>Election Outcome: </span>
          <span className="outcome-value">{getOutcomeText(conclusionContent?.effectiveness)}</span>
        </div>
        <h3>Counternarrative Strength</h3>
        <div className="effectiveness-bar">
          <div className={`segment red ${conclusionContent?.effectiveness?.toLowerCase() ? 'filled' : ''}`} />
          <div className={`segment yellow ${conclusionContent?.effectiveness?.toLowerCase() === 'medium' ? 'filled' : ''}`} />
          <div className={`segment green ${conclusionContent?.effectiveness?.toLowerCase() === 'strong' ? 'filled' : ''}`} />
        </div>
        <h3>Conclusion</h3>
        {isLoadingConclusion ? (
          <LoadingIcon />
        ) : (
          <p>{conclusionContent?.election_outcome}</p>
        )}
      </div>
      <div className="right-section">
        <h3>Counternarrative</h3>
        <div className="conclusion-custom-box">
          <NarrativeBox narrative={selectedCounterNarrative} isSelected={true} disabled={true} container="center" />
        </div>
        <div className="conclusion-custom-box">
          <CounterStratBox counterstrat={formattedSelectedCounterStrat} isSelected={true} disabled={true} container="center" />
        </div>
        <h3>Narrative</h3>
        <div className="conclusion-custom-box">
          <NarrativeBox narrative={selectedNarrative} isSelected={true} disabled={true} container="center" />
        </div>
        <div className="conclusion-custom-box">
          <StratBox strat={formattedSelectedStrat} isSelected={true} disabled={true} container="center" />
        </div>
        <div className="retry-button-container">
          {conclusionContent?.effectiveness !== 'strong' ? (
            <button onClick={handleButtonClick}>{t('common.retry')}</button>
          ) : (
            <>
              <p>{t('common.chooseWeakerStrategyMessage')}</p>
              <button onClick={handleButtonClick}>{t('common.goBack')}</button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConclusionWrapUp;