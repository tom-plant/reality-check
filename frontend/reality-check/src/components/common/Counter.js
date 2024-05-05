// Counter.js in components/common

import React from 'react';
import { useGameState } from '../../contexts/GameContext'; // Adjust the path as needed

const Counter = () => {
  const { selectedFactCombination, selectedStrat, selectedCounterStrat, currentView } = useGameState();

  // Determine which array to use based on the current view
  let items = selectedFactCombination;
  let divisor = 5;

  if (currentView === 'BUILD_NARRATIVE') {
    items = selectedStrat;
    divisor = 2;
  } else if (currentView === 'IDENTIFY_STRATEGIES') {
    items = selectedCounterStrat;
    divisor = 2; // Using 2 as specified
  }

  return (
    <div className="counter">
      {`${items.length}/${divisor} selected`}
    </div>
  );
};

export default Counter;