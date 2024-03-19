// SelectedFacts.js
import React, { useState, useEffect } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext'; // Adjust the path as needed
import FactBox from '../common/FactBox'; // Adjust the path as needed
import Counter from '../common/Counter'; // Adjust the path as needed
import Timer from '../common/Timer'; // Import the Timer component
import './SelectFacts.css'; // Ensure you have a CSS file for styling

const SelectFacts = () => {
  const { facts, selectedFactCombination, selectionEnded } = useGameState();
  const dispatch = useGameDispatch();
  const [displayedFacts, setDisplayedFacts] = useState(facts.slice(0, 5)); // Start with the first 5 facts

  useEffect(() => {
    // Initially load a random selection of 5 facts
    setDisplayedFacts(getRandomFacts(facts, 5));
  }, [facts]);

  const getRandomFacts = (factsArray, count) => {
  // Get a random selection of facts
    let shuffled = [...factsArray].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  };

  const loadMoreFacts = () => {
    if (selectionEnded) {
      return;
    }
    // Combine current displayed facts with a new random selection of 5 facts, excluding duplicates
    const newSelection = getRandomFacts(facts.filter(fact => !displayedFacts.includes(fact)), 5);
    setDisplayedFacts(prev => [...prev, ...newSelection]);
  };

  const onTimeUp = () => {
    dispatch({ type: 'SET_SELECTION_ENDED', payload: true });
    // Optional: Automatically select additional facts to meet the minimum requirement, if necessary
  };

  return (
    <div className="select-facts">
      <Timer onTimeUp={onTimeUp} />
      <Counter />  
      {displayedFacts.map((fact) => (
        <FactBox 
          key={fact.id}
          fact={fact}
          isSelected={selectedFactCombination.includes(fact)}
          disabled={selectionEnded} 
          container= "left"
        />
      ))}
      <button 
        className="load-more" 
        onClick={loadMoreFacts}
        disabled={selectionEnded} 
      >
        More Information
      </button>
    </div>
  );
};

export default SelectFacts;


//Within your game phase components (e.g., SelectFacts, SelectNarratives), 
// use the passed goToNextPhase function to transition to the next phase upon certain actions, 
// like selecting a fact or confirming a narrative.