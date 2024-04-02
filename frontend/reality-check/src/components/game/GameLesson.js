import React from 'react';
import { useTranslation } from 'react-i18next';
import './GameLesson.css'; // Import the CSS file

const GameLesson = () => {
  const { t } = useTranslation();

  return (
    <div className="game-lesson">
      <h2>{t('gameLesson.title')}</h2>
      <p className="introduction">{t('gameLesson.introduction')}</p>
      <p className="conclusion">{t('gameLesson.conclusion')}</p>
    </div>
  );
};

export default GameLesson;
