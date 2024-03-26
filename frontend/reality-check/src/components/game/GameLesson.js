import React from 'react';

const GameLesson = ({ setCurrentPhase }) => {
  return (
    <div className="game-lesson">
      <h2>Game Lesson</h2>
      <p>This is the part of the game where you reflect on the gameplay and share insights or lessons that can be taken away from the experience.</p>
      <button onClick={() => setCurrentPhase('intro')}>Restart Game</button>
    </div>
  );
};

export default GameLesson;