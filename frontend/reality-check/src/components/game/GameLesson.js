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
      <p className="posttest-link">
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSek5sDXTSsKEcck03iNVLTn5IkWimi3zr64p6qO7YTMy2c4Gw/viewform" target="_blank" rel="noopener noreferrer">
          {t('common.posttest')}
        </a>
      </p>
    </div>
  );
};

export default GameLesson;
