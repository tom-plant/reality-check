// src/context/GameContext.js
import React, { createContext, useContext, useReducer } from 'react';

const GameStateContext = createContext();
const GameDispatchContext = createContext();

const initialState = {
  facts: [
    { id: 1, text: 'Fact 1' },
    { id: 2, text: 'Fact 2' },
    { id: 3, text: 'Fact 3' },
    { id: 4, text: 'Fact 4' },
    { id: 5, text: 'Fact 5' },
    { id: 6, text: 'Fact 6' },
    { id: 7, text: 'Fact 7' },
    { id: 8, text: 'Fact 8' },
    { id: 9, text: 'Fact 9' },
    { id: 10, text: 'Fact 10' },
    { id: 11, text: 'Fact 11' },
    { id: 12, text: 'Fact 12' },
    { id: 13, text: 'Fact 13' },
    { id: 14, text: 'Fact 14' },
    { id: 15, text: 'Fact 15' },
    { id: 16, text: 'Fact 16' },
  ],
  currentView: 'SELECT_FACTS', 
  selectedFactCombination: [], 
  updatedFactCombination: [],
  narrativeOptions: [], 
  primaryNarrative: null, 
  secondaryNarratve: null, 
  Event: null,
  buttonStatus: {},
  userLanguage: 'English', // User selected language, default to English
};


const gameReducer = (state, action) => {
  switch (action.type) {
    case 'SET_CURRENT_VIEW':
      return { ...state, currentView: action.payload };

    case 'SET_LANGUAGE':
      return { ...state, userLanguage: action.payload };

    case 'SELECT_FACT':
      return {
        ...state,
        selectedFactCombination: [...state.selectedFactCombination, action.payload],
      };

    case 'DESELECT_FACT':
      return {
        ...state,
        selectedFactCombination: state.selectedFactCombination.filter(fact => fact !== action.payload),
      };

    case 'LOAD_MORE_FACTS':
      // Placeholder for loading more facts logic
      console.log('LOAD_MORE_FACTS action triggered. Implement logic to load more facts here.');
      return state; // Return the current state unchanged for now

    case 'GENERATE_NEWS_CONTENT':
      // Assuming this action updates a state variable with more information. Adjust as needed.
      return { ...state, additionalInfo: action.payload };

    case 'GENERATE_NARRATIVE':
      // This would set some narrative based on previous selections or information
      return { ...state, narrativeOptions: action.payload };

    case 'SELECT_NARRATIVE':
      // Assuming you're setting a primary narrative from the options
      return { ...state, primaryNarrative: action.payload };

    case 'CONFIRM_NARRATIVE_SELECTION':
      // Confirming the narrative might finalize the choice and prevent further changes
      return { ...state, narrativeConfirmed: true };

    case 'GENERATE_EVENT_RESPONSE':
      // This could be generating a response to an event, stored in state
      return { ...state, eventResponse: action.payload };

    case 'SELECT_UPDATED_FACT':
      return {
        ...state,
        updatedFactCombination: [...state.updatedFactCombination, action.payload],
      };

    case 'DESELECT_UPDATED_FACT':
      return {
        ...state,
        updatedFactCombination: state.updatedFactCombination.filter(fact => fact !== action.payload),
      };

    default:
      throw new Error(`Unhandled action type: ${action.type}`);
  }
};



const GameProvider = ({ children }) => {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  return (
    <GameStateContext.Provider value={state}>
      <GameDispatchContext.Provider value={dispatch}>
        {children}
      </GameDispatchContext.Provider>
    </GameStateContext.Provider>
  );
};

export const useGameState = () => useContext(GameStateContext);
export const useGameDispatch = () => useContext(GameDispatchContext);
export default GameProvider;
