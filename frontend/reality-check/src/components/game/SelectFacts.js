// SelectedFacts.js
import React, { useState, useEffect, useRef } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext'; // Adjust the path as needed
import FactBox from '../common/FactBox'; // Adjust the path as needed
import Counter from '../common/Counter'; // Adjust the path as needed
import Timer from '../common/Timer'; // Import the Timer component
import './SelectFacts.css'; // Ensure you have a CSS file for styling

const SelectFacts = () => {
  const { facts, selectedFactCombination, timerHasEnded, username, email } = useGameState();
  const { loginUser } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const [displayedFacts, setDisplayedFacts] = useState(facts.slice(0, 5)); // Start with the first 5 facts
  const selectedFactsRef = useRef(selectedFactCombination); // Ref to track the latest selected facts
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  useEffect(() => {
    selectedFactsRef.current = selectedFactCombination;
  }, [selectedFactCombination]);

  const onTimeUp = () => {
    setTimeout(() => {
      setIsButtonDisabled(true); // Disable the button
      dispatch({ type: 'SET_TIMER_ENDED', payload: true });
    }, 0);
  };

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
    if (timerHasEnded) {
      return;
    }
    // Combine current displayed facts with a new random selection of 5 facts, excluding duplicates
    const newSelection = getRandomFacts(facts.filter(fact => !displayedFacts.includes(fact)), 5);
    setDisplayedFacts(prev => [...prev, ...newSelection]);
  };

  const loginClick = async () => {
    await loginUser(username, email); // loginUser function from your context
    console.log('username', username)
    console.log('email', email)
  };

  // Step 3: Use useEffect to handle state updates after rendering
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
  }, [timerHasEnded, selectedFactsRef.current, dispatch, facts]); // Add dependencies as needed


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
      <button
        className='login'
        onClick={loginClick}
      >
        Login
      </button>
    </div>
  );
};

export default SelectFacts;

