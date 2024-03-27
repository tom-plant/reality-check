// IdentifyWeaknesses.js

import React, { useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import FactBox from '../common/FactBox';
import './IdentifyWeaknesses.css'; 

const IdentifyWeaknesses = () => {
  const { facts, updatedFactCombination, timerHasEnded } = useGameState();
  const [displayedFacts, setDisplayedFacts] = useState(facts);  

  return (
    <div className="identify-weaknesses">
      {displayedFacts.map(fact => (
        <FactBox
          key={fact.id}
          fact={fact}
          isSelected={updatedFactCombination.includes(fact)}
          disabled={timerHasEnded}
          container="left"
        />
      ))}
    </div>
  );
};

export default IdentifyWeaknesses;
