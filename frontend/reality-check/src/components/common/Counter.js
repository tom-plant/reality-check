// Counter.js in components/common

import React from 'react';
import { useGameState } from '../../contexts/GameContext'; // Adjust the path as needed

const Counter = () => {
  const { selectedFactCombination, facts } = useGameState();

  return (
    <div className="counter">
      {`${selectedFactCombination.length}/5 selected`}
    </div>
  );
};

export default Counter;
