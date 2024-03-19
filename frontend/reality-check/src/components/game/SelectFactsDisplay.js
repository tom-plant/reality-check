// SelectFactsDisplay.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import FactBox from '../common/FactBox'; 
import './SelectFactsDisplay.css';

const SelectFactsDisplay = () => {
  const { selectedFactCombination, selectionEnded } = useGameState();

  return (
    <div className="select-facts-display">
      <div className="spacer"></div>
      <div className="facts-list">
        {selectedFactCombination.map((fact) => (
          <FactBox 
            key={fact.id}
            fact={fact}
            isSelected={true} // These are always selected
            disabled={selectionEnded} 
            container="right"
          />
        ))}
      </div>
      <button className="generate-narrative" disabled={!selectionEnded}>
        Generate Narrative
      </button>
    </div>
  );
};


export default SelectFactsDisplay;






