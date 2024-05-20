//ConclusionWrapUp.js
import React, { useState, useEffect } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import LoadingIcon from '../common/LoadingIcon'; 
import StratBox from '../common/StratBox'; 
import CounterStratBox from '../common/CounterStratBox';
import NarrativeBox from '../common/NarrativeBox';
import './ConclusionWrapUp.css';

const ConclusionWrapUp = ({ setCurrentOutroView }) => {
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
      return 'Unknown';
    }

    switch (effectiveness.toLowerCase()) {
      case 'strong':
        return 'Peace';
      case 'medium':
        return 'Resolution';
      case 'weak':
        return 'Continued Crisis';
      default:
        return 'Unknown';
    }
  };


  // Determine which segments should be filled based on effectiveness
  const getFilledSegments = (effectiveness) => {
    if (!effectiveness) {
      return 0;
    }
    switch (effectiveness.toLowerCase()) {
      case 'strong':
        return 3;
      case 'medium':
        return 2;
      case 'weak':
        return 1;
      default:
        return 0;
    }
  };

  const filledSegments = getFilledSegments(conclusionContent?.effectiveness);


  return (
    <div className="conclusion-wrap-up">
      <div className="left-section">
        <h3>Did you preserve the peace?</h3>
        <div className="outcome-box">
          <span>Election Outcome: </span>
          <span className="outcome-value">{getOutcomeText(conclusionContent?.effectiveness)}</span>
        </div>
        <h3>Counternarrative Strength</h3>
        <div className="effectiveness-bar">
          <div className={`segment red ${filledSegments >= 1 ? 'filled' : ''}`} />
          <div className={`segment yellow ${filledSegments >= 2 ? 'filled' : ''}`} />
          <div className={`segment green ${filledSegments >= 3 ? 'filled' : ''}`} />
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
        <NarrativeBox narrative={selectedCounterNarrative} isSelected={true} disabled={true} container="left" />
        <CounterStratBox counterstrat={formattedSelectedCounterStrat} isSelected={true} disabled={true} />
        <NarrativeBox narrative={selectedNarrative} isSelected={true} disabled={true} container="right" />
        <StratBox strat={formattedSelectedStrat} isSelected={true} disabled={true} />
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