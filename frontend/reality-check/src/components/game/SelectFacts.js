import React, { useState, useEffect } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext'; // Adjust the path as needed
import FactBox from '../common/FactBox'; // Adjust the path as needed
import Counter from '../common/Counter'; // Adjust the path as needed
import Timer from '../common/Timer'; // Import the Timer component
import './SelectFacts.css'; // Ensure you have a CSS file for styling

const SelectFacts = () => {
  const { facts, selectedFactCombination } = useGameState();
  const dispatch = useGameDispatch();
  const [displayedFacts, setDisplayedFacts] = useState(facts.slice(0, 5)); // Start with the first 5 facts
  const [selectionEnded, setSelectionEnded] = useState(false);   // Add state to manage whether the selection phase has ended


  // Function to get a random selection of facts
  const getRandomFacts = (factsArray, count) => {
    let shuffled = [...factsArray].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  };

  useEffect(() => {
    // Initially load a random selection of 5 facts
    setDisplayedFacts(getRandomFacts(facts, 5));
  }, [facts]);

  const loadMoreFacts = () => {
    if (selectionEnded) {
      // Do nothing if selection phase has ended
      return;
    }
    // Combine current displayed facts with a new random selection of 5 facts, excluding duplicates
    const newSelection = getRandomFacts(facts.filter(fact => !displayedFacts.includes(fact)), 5);
    setDisplayedFacts(prev => [...prev, ...newSelection]);
  };

  const onTimeUp = () => {
    setSelectionEnded(true);
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
          onSelect={() => dispatch({ type: 'SELECT_FACT', payload: fact })}
          onDeselect={() => dispatch({ type: 'DESELECT_FACT', payload: fact })}
          disabled={selectionEnded} 
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