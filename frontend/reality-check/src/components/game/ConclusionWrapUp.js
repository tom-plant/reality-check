//ConclusionWrapUp.js
import React, { useState, useEffect } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import LoadingIcon from '../common/LoadingIcon'; 
import './ConclusionWrapUp.css';

const ConclusionWrapUp = ({ setCurrentOutroView }) => {
  const { conclusionContent, isLoadingConclusion } = useGameState();
  const { t } = useTranslation();
  const [buttonClicked, setButtonClicked] = useState(false); 

  // Set updated facts and generate updated news content
  const handleConclude = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      setCurrentOutroView('GAME_LESSON')}
    }

  return (
    <div className="conclusion-wrap-up">
      <h2>Game Conclusion</h2>
      <p className="conclusion-introduction"></p>
      {isLoadingConclusion ? (
        <LoadingIcon />
      ) : (
        <>
          <p>{conclusionContent?.election_outcome}</p> 
          <button onClick={handleConclude}>{t('common.continue')}</button>
        </>
      )}
    </div>
  );
};

export default ConclusionWrapUp;


