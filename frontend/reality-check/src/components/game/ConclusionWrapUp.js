import React from 'react';

const ConclusionWrapUp = ({ setCurrentOutroView }) => {
  return (
    <div className="conclusion-wrap-up">
      <h2>Game Conclusion</h2>
      <p>This is where the game wraps up, summarizing your journey, the decisions you made, and the outcomes of those decisions.</p>
      <button onClick={() => setCurrentOutroView('GAME_LESSON')}>Proceed to Game Lesson</button>
    </div>
  );
};

export default ConclusionWrapUp;
