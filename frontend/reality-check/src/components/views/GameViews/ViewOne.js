// ViewOne.Js

import React from 'react';
import { useGame } from '../../contexts/GameContext';


const ViewOne = () => {
    const { view, setView } = useGame(); // Access game state and updater function

  return (
    <div>
      {/* Content for View One */}
    </div>
  );
};

export default ViewOne;