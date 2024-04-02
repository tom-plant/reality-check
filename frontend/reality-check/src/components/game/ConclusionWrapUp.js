//ConclusionWrapUp.js
import React, { useState, useEffect } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';

const ConclusionWrapUp = ({ setCurrentOutroView }) => {
  const { conclusionContent, isLoadingConclusion } = useGameState();
  const { t } = useTranslation();
  const { fetchAndSetConclusion } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const [buttonClicked, setButtonClicked] = useState(false); 
  const [content, setContent] = useState(null);

  // Set updated facts and generate updated news content
  const handleConclude = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      setCurrentOutroView('GAME_LESSON')}
      fetchAndSetConclusion(); 
    }

  // Render news content from the backend
  useEffect(() => {
    if (conclusionContent && !isLoadingConclusion) {
      setContent(conclusionContent);
    }
  }, [conclusionContent, isLoadingConclusion]); 
  
  return (
    <div className="conclusion-wrap-up">
      <h2>Game Conclusion</h2>
      <p>{content}</p>
      <button onClick={handleConclude}>{t('common.continue')}</button>
    </div>
  );
};

export default ConclusionWrapUp;


