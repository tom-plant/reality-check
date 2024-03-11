//ViewTwo.Js

import React from 'react';
import { useGame } from '../../contexts/GameContext';

const ViewTwo = () => {
    const { view, setView } = useGame(); // Access game state and updater function


  return (
    <div>
      {/* Content for View Two */}
    </div>
  );
};

export default ViewTwo;