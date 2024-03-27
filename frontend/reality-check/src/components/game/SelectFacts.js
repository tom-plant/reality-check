// SelectedFacts.js

import React, { useState, useEffect, useRef } from 'react';
import { useGameState, useGameDispatch } from '../../contexts/GameContext'; 
import FactBox from '../common/FactBox'; 
import Counter from '../common/Counter';
import Timer from '../common/Timer'; 
import './SelectFacts.css'; 

const SelectFacts = () => {
  const { facts, selectedFactCombination, timerHasEnded } = useGameState();
  const dispatch = useGameDispatch();
  const [displayedFacts, setDisplayedFacts] = useState(facts.slice(0, 5)); 
  const selectedFactsRef = useRef(selectedFactCombination); 
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  useEffect(() => {
    selectedFactsRef.current = selectedFactCombination;
  }, [selectedFactCombination]);

  // Run out timer and disable More Information button
  const onTimeUp = () => {
    setTimeout(() => {
      setIsButtonDisabled(true); 
      dispatch({ type: 'SET_TIMER_ENDED', payload: true });
    }, 0);
  };

  // Pre-load a random selection of 5 facts
  useEffect(() => {
    setDisplayedFacts(getRandomFacts(facts, 5));
  }, [facts]);

// Get a random selection of facts
  const getRandomFacts = (factsArray, count) => {
    let shuffled = [...factsArray].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  };

// Allow rendering of additional facts
  const loadMoreFacts = () => {
    if (timerHasEnded) {
      return;
    }
    const newSelection = getRandomFacts(facts.filter(fact => !displayedFacts.includes(fact)), 5);
    setDisplayedFacts(prev => [...prev, ...newSelection]);
  };

// Autoselect additional facts
  useEffect(() => {
    if (timerHasEnded) {
      if (selectedFactsRef.current.length < 3) {
        const factsNeeded = 3 - selectedFactsRef.current.length;
        const unselectedFacts = facts.filter(fact => !selectedFactsRef.current.includes(fact));
        const additionalFacts = getRandomFacts(unselectedFacts, factsNeeded);

        additionalFacts.forEach(fact => {
          dispatch({ type: 'SELECT_FACT', payload: fact });
        });
      }
    }
  }, [timerHasEnded, selectedFactsRef.current, dispatch, facts]); 


  return (
    <div className="select-facts">
      <div className="timer-counter-wrapper">
        <Timer onTimeUp={onTimeUp} />
        <Counter />  
      </div> 
      <div className="facts-list">
        {displayedFacts.map((fact) => (
          <FactBox 
            key={fact.id}
            fact={fact}
            isSelected={selectedFactCombination.includes(fact)}
            disabled={timerHasEnded} 
            container= "left"
          />
        ))}
      </div>
      <button 
        className="load-more" 
        onClick={loadMoreFacts}
        disabled={isButtonDisabled} 
      >
        More Information
      </button>
    </div>
  );
};

export default SelectFacts;

