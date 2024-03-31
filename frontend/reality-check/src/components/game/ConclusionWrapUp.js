//ConclusionWrapUp.js
import { useTranslation } from 'react-i18next';
import React from 'react';

const ConclusionWrapUp = ({ setCurrentOutroView }) => {
  const { t } = useTranslation();

  return (
    <div className="conclusion-wrap-up">
      <h2>Game Conclusion</h2>
      <p>This is where the game wraps up, summarizing your journey, the decisions you made, and the outcomes of those decisions.</p>
      <button onClick={() => setCurrentOutroView('GAME_LESSON')}>{t('common.continue')} </button>
    </div>
  );
};

export default ConclusionWrapUp;
