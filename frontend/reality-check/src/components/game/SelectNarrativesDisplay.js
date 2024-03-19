// SelectNarrativesDisplay.js
import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import './SelectNarrativesDisplay.css'; // Create a new CSS file for this component

const SelectNarrativesDisplay = () => {
  const { selectedFactCombination } = useGameState();

  return (
    <div className="select-narratives-display">
      <h2>Selected Facts</h2>
      <div className="facts-list">
        {selectedFactCombination.map((fact) => (
          <div key={fact.id} className="displayed-fact">
            {fact.text}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SelectNarrativesDisplay;
