// src/context/GameContext.js
import React, { createContext, useContext, useReducer, useState, useEffect } from 'react';
import { authenticateUser, getFacts, getEvents, generateNarrativeFromFacts, selectNarrative, introduceEvent } from '../services/gameService';

const GameStateContext = createContext();
const GameDispatchContext = createContext();
const GameFunctionContext = createContext(); // Create a new context for functions

const initialState = {
  currentView: 'SELECT_FACTS', 
  username: 'tomtom',
  email: 'lolita@gmail.com',
  facts: [],
  events: [],
  selectedFactCombination: [],
  timerHasEnded: false, 
  isLoadingNarratives: false,
  isLoadingNews: false,
  narrativeOptions: [],
  selectedNarrative: [],
  primaryNewsContent: null,
  selectedEvent: null,
  eventNewsContent: null,
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

    case 'SET_USER':
      return { ...state, user: action.payload };
  
    case 'SET_EMAIL':
      return { ...state, email: action.payload };

    case 'SET_AUTH_ERROR':
      return { ...state, authError: action.payload };
      
    case 'SET_LANGUAGE':
      return { ...state, userLanguage: action.payload };

    case 'SET_FACTS':
      return {
        ...state,
        facts: action.payload, 
      };
  
    case 'SET_EVENTS':
      return {
        ...state,
        events: action.payload, 
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

    case 'SET_NARRATIVE_OPTIONS':
      return {
        ...state,
        narrativeOptions: action.payload, 
      };
  
    case 'SET_LOADING_NARRATIVES':
      return { ...state, isLoadingNarratives: action.payload };

    case 'SET_LOADING_NEWS':
      return { ...state, isLoadingNews: action.payload };

    case 'SET_SELECTED_NARRATIVE_CONTENT':
      return { ...state, primaryNewsContent: action.payload };

    case 'SET_EVENT_NEWS_CONTENT':
      return { ...state, eventNewsContent: action.payload };
  
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

  const fetchAndSetEvents = async () => {
    try {
      const response = await getEvents(); // Assuming this returns the full response
      if (response && response.events) {
        const eventsData = response.events;
        const transformedEvents = eventsData.map(event => ({
          id: event.id,
          text: event.text
        }));
        dispatch({ type: 'SET_EVENTS', payload: transformedEvents });
      } else {
        console.error("Fetched data is not in the expected format:", response);
      }
    } catch (error) {
      console.error("Failed to fetch events:", error);
    }
  };
  
  useEffect(() => {
    fetchAndSetFacts();
    fetchAndSetEvents();
  }, []); 

  // Inside your GameProvider component or function where you define custom context functions
  const loginUser = async (username, email) => {
    try {
      const response = await authenticateUser(username, email);
      // Dispatch an action to update your state based on the response
      // For example, storing the user_id in the state
      dispatch({ type: 'SET_USER', payload: response.user_id });
    } catch (error) {
      console.error("Authentication error:", error);
      // Handle error, possibly by setting an error message in your state
      dispatch({ type: 'SET_AUTH_ERROR', payload: error.message });
    }
  };


  const fetchAndSetNarratives = async (selectedFacts) => {
    try {
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: true });
      const narrativesData = await generateNarrativeFromFacts(selectedFacts);
      // Map the narratives to the expected format
      const formattedNarratives = narrativesData.narratives.map((narrativeText, index) => ({
        id: index, // Since there might not be unique IDs, using index as a key
        text: narrativeText
      }));
      dispatch({ type: 'SET_NARRATIVE_OPTIONS', payload: formattedNarratives });
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
    } catch (error) {
      console.error("Failed to fetch narratives:", error);
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
    }
  };


  // Context function to select a narrative
  const selectNarrativeAndSetContent = async (selectedNarrative) => {
    try {
      dispatch({ type: 'SET_LOADING_NEWS', payload: true }); 
      const content = await selectNarrative(selectedNarrative);
      dispatch({ type: 'SET_SELECTED_NARRATIVE_CONTENT', payload: content });
      dispatch({ type: 'SET_LOADING_NEWS', payload: false });
    } catch (error) {
      console.error('Failed to select narrative:', error);
      dispatch({ type: 'SET_LOADING_NEWS', payload: false });
    }
  };

  const selectEventAndSetContent = async (selectedEvent) => {
    try {
      dispatch({ type: 'SET_LOADING_NEWS', payload: true }); 
      console.log('selectedevent in the context function is: ', selectedEvent)
      const content = await introduceEvent(selectedEvent);
      console.log('response in context is: ',content)
      dispatch({ type: 'SET_EVENT_NEWS_CONTENT', payload: content });
      dispatch({ type: 'SET_LOADING_NEWS', payload: false }); 
    } catch (error) {
      console.error('Failed to introduce event:', error);
      dispatch({ type: 'SET_LOADING_NEWS', payload: false }); 
      // Handle error, e.g., by setting an error state
    }
  };

  return (
    <GameStateContext.Provider value={state}>
      <GameDispatchContext.Provider value={dispatch}>
        <GameFunctionContext.Provider value={{ fetchAndSetFacts, fetchAndSetEvents, loginUser, fetchAndSetNarratives, selectNarrativeAndSetContent, selectEventAndSetContent }}> 
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
