// src/context/GameContext.js

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authenticateUser, getFacts, getEvents, generateNarrativeFromFacts, selectNarrative, introduceEvent, identifyWeaknesses } from '../services/gameService';

const GameStateContext = createContext();
const GameDispatchContext = createContext();
const GameFunctionContext = createContext(); 

const initialState = {
  currentPhase: 'intro', 
  currentIntroView: 'AUTH_LOGIN',
  currentView: 'IDENTIFY_WEAKNESSES', 
  currentTurnPointView: 'ALERT',
  currentOutroView: 'CONCLUSION_WRAP_UP',
  username: null,
  email: null,
  facts: [],
  events: [],
  selectedFactCombination: [],
  updatedFactCombination: [],
  narrativeOptions: [],
  selectedNarrative: null,
  secondaryNarrative: [],
  selectedEvent: null,
  primaryNewsContent: null,
  eventNewsContent: null,
  secondaryNewsContent: null,
  isUpdatedNarrativePopupVisible: false,
  isIntroPopupVisibile: true,
  timerHasEnded: false, 
  isLoadingNarratives: false,
  isLoadingNews: false,
  userLanguage: 'English', 
};


const gameReducer = (state, action) => {
  switch (action.type) {

    case 'SET_CURRENT_PHASE':
      return { ...state, currentPhase: action.payload };

    case 'SET_CURRENT_INTRO_VIEW':
      return { ...state, currentIntroView: action.payload };

    case 'SET_CURRENT_TURN_POINT_VIEW':
      return { ...state, currentTurnPointView: action.payload };

    case 'SET_CURRENT_OUTRO_VIEW':
      return { ...state, currentOutroView: action.payload };

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
      return { ...state, selectedNarrative: action.payload };

    case 'DESELECT_NARRATIVE':
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

    case 'SET_SECONDARY_NARRATIVE_CONTENT':
      return { 
        ...state, 
        secondaryNewsContent: action.payload 
      };
  
    case 'SET_SECONDARY_NARRATIVE':
      return { ...state, secondaryNarrative: action.payload };
      
    case 'SELECT_EVENT':
      return { ...state, selectedEvent: action.payload };

    case 'DESELECT_EVENT':
      return { ...state, selectedEvent: action.payload };

    case 'SET_EVENT_OPTIONS':
      return { ...state, eventOptions: action.payload };

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

    case 'SET_UPDATED_NARRATIVE':
      return {
        ...state,
        secondaryNarrative: action.payload,
      };
      
    case 'TOGGLE_UPDATED_NARRATIVE_POPUP':
      return { ...state, isUpdatedNarrativePopupVisible: !state.isUpdatedNarrativePopupVisible };

    case 'TOGGLE_INTRO_POPUP':
      return { ...state, isIntroPopupVisible: !state.isIntroPopupVisible };

      default:
        throw new Error(`Unhandled action type: ${action.type}`);
    }
};


const GameProvider = ({ children }) => {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  // Game transitioning

  const setCurrentPhase = (phase) => {
    dispatch({ type: 'SET_CURRENT_PHASE', payload: phase });
  };

  const setCurrentIntroView = (view) => {
    dispatch({ type: 'SET_CURRENT_INTRO_VIEW', payload: view });
  };

  const setCurrentTurnPointView = (view) => {
    dispatch({ type: 'SET_CURRENT_TURN_POINT_VIEW', payload: view });
  };

  const setCurrentOutroView = (view) => {
    dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: view });
  };

  // API Calls

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

  const loginUser = async (username, email) => {
    try {
      const response = await authenticateUser(username, email);
      dispatch({ type: 'SET_USER', payload: response.user_id });
    } catch (error) {
      console.error("Authentication error:", error);
      dispatch({ type: 'SET_AUTH_ERROR', payload: error.message });
    }
  };


  const fetchAndSetNarratives = async (selectedFacts) => {
    try {
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: true });
      const narrativesData = await generateNarrativeFromFacts(selectedFacts);
      const formattedNarratives = narrativesData.narratives.map((narrativeText, index) => ({
        id: index, 
        text: narrativeText
      }));
      dispatch({ type: 'SET_NARRATIVE_OPTIONS', payload: formattedNarratives });
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
    } catch (error) {
      console.error("Failed to fetch narratives:", error);
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
    }
  };


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
      const content = await introduceEvent(selectedEvent);
      dispatch({ type: 'SET_EVENT_NEWS_CONTENT', payload: content });
      dispatch({ type: 'SET_LOADING_NEWS', payload: false }); 
    } catch (error) {
      console.error('Failed to introduce event:', error);
      dispatch({ type: 'SET_LOADING_NEWS', payload: false }); 
    }
  };

  const identifyWeaknessesAndSetContent = async (updatedFactCombination) => {
    try {
      dispatch({ type: 'SET_LOADING_NEWS', payload: true }); 
        const response = await identifyWeaknesses(updatedFactCombination);
        dispatch({
          type: 'SET_SECONDARY_NARRATIVE_CONTENT',
          payload: {
            secondary_news_content: response.secondary_news_content
          }
        });        
        dispatch({ type: 'SET_SECONDARY_NARRATIVE', payload: response.secondary_narrative });
      dispatch({ type: 'SET_LOADING_NEWS', payload: false });
    } catch (error) {
      console.error('Failed to identify weaknesses:', error);
      dispatch({ type: 'SET_LOADING_NEWS', payload: false }); 
    }
  };
  return (
    <GameStateContext.Provider value={state}>
      <GameDispatchContext.Provider value={dispatch}>
        <GameFunctionContext.Provider value={{ fetchAndSetFacts, fetchAndSetEvents, loginUser, fetchAndSetNarratives, selectNarrativeAndSetContent, selectEventAndSetContent, identifyWeaknessesAndSetContent, setCurrentPhase, setCurrentOutroView, setCurrentTurnPointView, setCurrentIntroView }}> 
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
