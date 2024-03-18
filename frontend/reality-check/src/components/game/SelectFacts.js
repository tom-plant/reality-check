import React from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext'; // Adjust the path as needed
import FactBox from '../common/FactBox'; // Adjust the path as needed
import './SelectFacts.css'; // Ensure you have a CSS file for styling

const SelectFacts = () => {
  const { facts, selectedFactCombination } = useGameState();
  const dispatch = useGameDispatch();
  
  const loadMoreFacts = () => {
    // Dispatch an action to load more facts
    // For now, let's just log a message. Replace this with actual logic to load more facts.
    console.log('Load more facts...');
    // dispatch({ type: 'LOAD_MORE_FACTS' });
  };

  return (
    <div className="select-facts">
      {facts.map((fact) => (
        <FactBox 
          key={fact.id} // Ensure each fact has a unique identifier
          fact={fact}
          isSelected={selectedFactCombination.includes(fact)}
        />
      ))}
      <button className="load-more" onClick={loadMoreFacts}>
        More Information
      </button>
    </div>
  );
};

export default SelectFacts;


//Within your game phase components (e.g., SelectFacts, SelectNarratives), 
// use the passed goToNextPhase function to transition to the next phase upon certain actions, 
// like selecting a fact or confirming a narrative.