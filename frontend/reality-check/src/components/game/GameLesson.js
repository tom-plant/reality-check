import React from 'react';
import { useTranslation } from 'react-i18next'; 

const GameLesson = () => {
  const { t } = useTranslation();

  return (
    <div className="game-lesson">
      <h2>Game Lesson</h2>
      <p>This is the part of the game where you reflect on the gameplay and share insights or lessons that can be taken away from the experience.</p>
    </div>
  );
};

export default GameLesson;
