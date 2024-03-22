// IdentifyWeaknesses.js
import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext';
import FactBox from '../common/FactBox';
import './IdentifyWeaknesses.css'; // Ensure you have this CSS file

const IdentifyWeaknesses = () => {
  const { facts, updatedFactCombination, selectionEnded } = useGameState();
  const [displayedFacts, setDisplayedFacts] = useState(facts);  // Display all facts

  return (
    <div className="identify-weaknesses">
      {displayedFacts.map(fact => (
        <FactBox
          key={fact.id}
          fact={fact}
          isSelected={updatedFactCombination.includes(fact)}
          disabled={selectionEnded}
          container="left"
        />
      ))}
    </div>
  );
};

export default IdentifyWeaknesses;
