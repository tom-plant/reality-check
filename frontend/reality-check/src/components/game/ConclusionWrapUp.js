//ConclusionWrapUp.js
import React, { useState, useEffect } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import LoadingIcon from '../common/LoadingIcon'; 
import './ConclusionWrapUp.css';

const ConclusionWrapUp = ({ setCurrentOutroView }) => {
  const { conclusionContent, isLoadingConclusion } = useGameState();
  const { t } = useTranslation();
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 

  // Set updated facts and generate updated news content
  const handleConclude = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      setCurrentOutroView('GAME_LESSON')}
    }

  // Fetch the introduction text from the translation file
  const introductionText = t('conclusionWrapUp.introduction');

  return (
    <div className="conclusion-wrap-up">
      <h2>Game Conclusion</h2>
      <p className="conclusion-introduction">{introductionText}</p> {/* Display the introduction text */}
      {isLoadingConclusion ? (
        <LoadingIcon />
      ) : (
        <>
          {conclusionContent?.conclusion_paragraphs?.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
          <button onClick={handleConclude}>{t('common.continue')}</button>
        </>
      )}
    </div>
  );
};

export default ConclusionWrapUp;



