// src/context/GameContext.js
import React, { createContext, useContext, useReducer, useState, useEffect } from 'react';
import { getFacts } from '../services/gameService';

const GameStateContext = createContext();
const GameDispatchContext = createContext();
const GameFunctionContext = createContext(); // Create a new context for functions

const initialState = {
  facts: [],
  currentView: 'SELECT_FACTS', 
  selectedFactCombination: [],
  timerHasEnded: false, 
  narrativeOptions: [
    { id: 1, text: "Two glasses of milk, please." },
    { id: 2, text: "I said, TWO GLASSES OF MILK, please." },
    { id: 3, text: "You know what, forget it." }
  ],
  selectedNarrative: [
    { id: 1, text: "I am a C-H-R-I-S-T-I-A-N"}
  ],
  primaryNewsContent: {
    headline: 'Bruh literally edged in fortnite.',
    story: 'Late yesterday evening, bruh literally edged in a fortnite game, shocking thousands and coming amidst a time of extreme scrutiny toward edging and and overwhelming preference to gooning. Literally bruh.',
    imageUrl: 'ayoooooplaceholder.com'
  },
  primaryNarrative: null, 
  eventOptions: [
    { id: 1, text: "Event 1"},
    { id: 2, text: "Event 2"},
    { id: 3, text: "Event 3"}
  ],
  selectedEvent: null,
  updatedFactCombination: [],
  secondaryNarrative: { id: 1, text: "kaksteist kuud" } ,
  isUpdatedNarrativePopupVisible: false,
  secondaryNewsContent: {
    headline: "5 tips to rizz up your crush",
    story: '1) Let me show you what these paws can do, 2) r/nevertellmetheodds of us meeting, 3) le epic sigma mogging, 4) can I get a huh yeah? 5) gigachad. nuff said.',
    imageUrl: 'ayoooooplaceholder.com'
  },
  userLanguage: 'English', // User selected language, default to English
};


const gameReducer = (state, action) => {
  switch (action.type) {
    case 'SET_CURRENT_VIEW':
      return { ...state, currentView: action.payload };

    case 'SET_LANGUAGE':
      return { ...state, userLanguage: action.payload };

    case 'SET_FACTS':
      return {
        ...state,
        facts: action.payload, 
      };

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

    case 'COPY_FACTS_TO_UPDATED':
      return {
        ...state,
        updatedFactCombination: action.payload,
      };

    case 'ADD_FACTS':
      return {
        ...state,
        selectedFactCombination: [...state.selectedFactCombination, ...action.payload],
      };

    case 'SET_TIMER_ENDED':
      return { ...state, timerHasEnded: action.payload };  

    case 'SELECT_NARRATIVE':
      console.log('Selecting narrative:', action.payload);
      return { ...state, selectedNarrative: action.payload };

    case 'DESELECT_NARRATIVE':
      console.log('Deselecting narrative');
      return { ...state, selectedNarrative: null };

    case 'SET_NEWS_CONTENT':
      return {
        ...state,
        primaryNewsContent: action.payload // Assuming payload will be an object with headline, story, and imageUrl
      };

    case 'SELECT_EVENT':
      return { ...state, selectedEvent: action.payload };

    case 'DESELECT_EVENT':
      return { ...state, selectedEvent: action.payload };

    case 'SET_EVENT_OPTIONS':
      return { ...state, eventOptions: action.payload };

    case 'GENERATE_NEWS_CONTENT':
      // Assuming this action updates a state variable with more information. Adjust as needed.
      return { ...state, additionalInfo: action.payload };

    case 'GENERATE_NARRATIVE':
      // This would set some narrative based on previous selections or information
      return { ...state, narrativeOptions: action.payload };

    case 'CONFIRM_NARRATIVE_SELECTION':
      // Confirming the narrative might finalize the choice and prevent further changes
      return { ...state, narrativeConfirmed: true };

    case 'GENERATE_EVENT_RESPONSE':
      // This could be generating a response to an event, stored in state
      return { ...state, eventResponse: action.payload }

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

    case 'RESET_SELECTION_ENDED':
      return {
        ...state,
        timerHasEnded: false,
      };

    case 'UPDATE_FACTS':
      return {
        ...state,
        updatedFactCombination: action.payload,
      };

    // case 'GENERATE_UPDATED_NARRATIVE':
    //   return {
    //     ...state,
    //     secondaryNarrative: action.payload,
    //   };

    case 'SET_UPDATED_NARRATIVE':
      return {
        ...state,
        secondaryNarrative: action.payload,
      };
      
    case 'TOGGLE_UPDATED_NARRATIVE_POPUP':
      return { ...state, isUpdatedNarrativePopupVisible: !state.isUpdatedNarrativePopupVisible };

      default:
        throw new Error(`Unhandled action type: ${action.type}`);
    }
};


const GameProvider = ({ children }) => {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  const fetchAndSetFacts = async () => {
    try {
      const response = await getFacts(); // Assuming this returns the full response
      if (response && response.facts) {
        const factsData = response.facts;
        const transformedFacts = factsData.map(fact => ({
          id: fact.id,
          text: fact.text
        }));
        dispatch({ type: 'SET_FACTS', payload: transformedFacts });
      } else {
        console.error("Fetched data is not in the expected format:", response);
      }
    } catch (error) {
      console.error("Failed to fetch facts:", error);
    }
  };

  useEffect(() => {
    // Call fetchAndSetFacts within useEffect
    fetchAndSetFacts();
  }, []); // Empty dependency array means this effect runs once on mount


  return (
    <GameStateContext.Provider value={state}>
      <GameDispatchContext.Provider value={dispatch}>
        <GameFunctionContext.Provider value={{ fetchAndSetFacts }}> 
          {children}
          </GameFunctionContext.Provider>
      </GameDispatchContext.Provider>
    </GameStateContext.Provider>
  );
};

export const useGameState = () => useContext(GameStateContext);
export const useGameDispatch = () => useContext(GameDispatchContext);
export const useGameFunction = () => useContext(GameFunctionContext); 

export default GameProvider;
