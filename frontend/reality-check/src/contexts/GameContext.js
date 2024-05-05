// src/context/GameContext.js

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authenticateUser, getFacts, getEvents, getActors, getStrats, getCounterStrats, setSelectedFacts, buildNarrative, selectNarrative, introduceEvent, identifyWeaknesses, conclusion } from '../services/gameService';

const GameStateContext = createContext();
const GameDispatchContext = createContext();
const GameFunctionContext = createContext(); 

const initialState = {
  currentPhase: 'intro', 
  currentIntroView: 'AUTH_LOGIN',
  currentView: 'SELECT_FACTS', 
  currentTurnPointView: 'ALERT',
  currentOutroView: 'CONCLUSION_WRAP_UP',
  username: null,
  email: null,
  facts: [],
  events: [],
  actors: [],
  strats: [],
  counterstrats: [],
  selectedFactCombination: [],
  updatedFactCombination: [],
  narrativeOptions: [],
  counterNarrativeOptions: [],
  selectedNarrative: null,
  selectedCounterNarrative: [],
  secondaryNarrative: [],
  conclusionContent: [],
  selectedEvent: null,
  selectedStrat: [],
  selectedCounterStrat: [],
  selectedActor: [],
  primaryNewsContent: null,
  eventNewsContent: null,
  secondaryNewsContent: null,
  isUpdatedNarrativePopupVisible: false,
  isIntroPopupVisibile: true,
  timerHasEnded: false, 
  isLoadingNarratives: false,
  isLoadingNews: false,
  isLoadingConclusion: false,
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
  
    case 'SET_ACTORS':
      return {
        ...state,
        actors: action.payload, 
      };
  
    case 'SET_STRATS':
      return {
        ...state,
        strats: action.payload, 
      };

    case 'SET_COUNTERSTRATS':
      return {
        ...state,
        counterstrats: action.payload, 
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

    case 'SELECT_COUNTERNARRATIVE':
      return { ...state, selectedCounterNarrative: action.payload };

    case 'DESELECT_COUNTERNARRATIVE':
      return { ...state, selectedCounterNarrative: null };

    case 'SET_NARRATIVE_OPTIONS':
      return {
        ...state,
        narrativeOptions: action.payload, 
      };

    case 'SET_COUNTERNARRATIVE_OPTIONS':
      return {
        ...state,
        counterNarrativeOptions: action.payload, 
      };    
  
    case 'SET_LOADING_NARRATIVES':
      return { ...state, isLoadingNarratives: action.payload };

    case 'SET_LOADING_NEWS':
      return { ...state, isLoadingNews: action.payload };

    case  'SET_LOADING_CONCLUSION':
      return { ...state, isLoadingConclusion: action.payload };

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
      
    case 'SET_CONCLUSION_CONTENT':
      return { ...state, conclusionContent: action.payload };

    case 'SELECT_EVENT':
      return { ...state, selectedEvent: action.payload };

    case 'DESELECT_EVENT':
      return { ...state, selectedEvent: action.payload };

    case 'SELECT_ACTOR':
      return { ...state, selectedActor: action.payload };

    case 'DESELECT_ACTOR':
      return { ...state, selectedActor: action.payload };

    case 'SELECT_STRAT':
      return { ...state, 
        selectedStrat: [...state.selectedStrat, action.payload],
      };

    case 'DESELECT_STRAT':
      return { ...state, 
        selectedStrat: state.selectedStrat.filter(strat => strat !== action.payload),
      };

    case 'SELECT_COUNTERSTRAT':
      return { ...state, 
        selectedCounterStrat: [...state.selectedCounterStrat, action.payload],
      };
    case 'DESELECT_COUNTERSTRAT':
      return { ...state, 
        selectedCounterStrat: state.selectedCounterStrat.filter(counterstrat => counterstrat !== action.payload),
      };
      
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
  
  const fetchAndSetActors = async () => {
    try {
      const response = await getActors(); 
      if (response && response.actors) {
        const actorsData = response.actors;
        const transformedActors = actorsData.map(actor => ({
          id: actor.id,
          text: actor.text
        }));
        dispatch({ type: 'SET_ACTORS', payload: transformedActors });
      } else {
        console.error("Fetched data is not in the expected format:", response);
      }
    } catch (error) {
      console.error("Failed to fetch actors:", error);
    }
  };
  
  const fetchAndSetStrats = async () => {
    try {
      const response = await getStrats(); 
      if (response && response.strats) {
        const stratsData = response.strats;
        const transformedStrats = stratsData.map(strat => ({
          id: strat.id,
          text: strat.text
        }));
        dispatch({ type: 'SET_STRATS', payload: transformedStrats });
      } else {
        console.error("Fetched data is not in the expected format:", response);
      }
    } catch (error) {
      console.error("Failed to fetch strats:", error);
    }
  };

  const fetchAndSetCounterStrats = async () => {
    try {
      const response = await getCounterStrats(); 
      if (response && response.counterstrats) {
        const counterstratsData = response.counterstrats;
        const transformedCounterStrats = counterstratsData.map(counterstrats => ({
          id: counterstrats.id,
          text: counterstrats.text
        }));
        dispatch({ type: 'SET_COUNTERSTRATS', payload: transformedCounterStrats });
      } else {
        console.error("Fetched data is not in the expected format:", response);
      }
    } catch (error) {
      console.error("Failed to fetch counterstrats:", error);
    }
  };

  useEffect(() => {
    fetchAndSetFacts();
    fetchAndSetEvents();
    fetchAndSetActors();
    fetchAndSetStrats();
    fetchAndSetCounterStrats();
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

  const setFactSelection = async (selectedFacts) => {
    try {
      // Simply send the selected facts to the backend
      await setSelectedFacts(selectedFacts);
    } catch (error) {
      console.error("Failed to set selected facts:", error);
    }
  };

  const buildAndSetNarrative = async (selectedActor, selectedStrategies) => {
    try {
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: true });
      const narrativeResponse = await buildNarrative(selectedActor, selectedStrategies);
      const formattedNarratives = Object.keys(narrativeResponse).map((strategy, index) => ({
        id: index,
        text: narrativeResponse[strategy],
        strategy: strategy  // Include the strategy in the narrative data
      }));
      dispatch({ type: 'SET_NARRATIVE_OPTIONS', payload: formattedNarratives });
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
    } catch (error) {
      console.error('Failed to build narrative:', error);
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
    }
  };

  const selectNarrativeAndSetContent = async (selectedNarrative) => {
    try {
      dispatch({ type: 'SET_LOADING_NEWS', payload: true }); 
      const content = await selectNarrative({
        narrative: selectedNarrative.text,
        strategy: selectedNarrative.strategy //not sure if this is actually a part of what selectedNarrative actually is
      });
      dispatch({ type: 'SET_SELECTED_NARRATIVE_CONTENT', payload: content });
      console.log('received narrative news content in context', content)
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

  const identifyWeaknessesAndSetContent = async (updatedFactCombination, selectedStrategies) => {
    try {
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: true });
      const weaknessesResponse = await identifyWeaknesses(updatedFactCombination, selectedStrategies);
      const formattedCounterNarratives = Object.keys(weaknessesResponse).map((strategy, index) => ({
        id: index,
        text: weaknessesResponse[strategy],
        strategy: strategy  // Keeping track of which strategy each narrative corresponds to
      }));
      dispatch({ type: 'SET_COUNTERNARRATIVE_OPTIONS', payload: formattedCounterNarratives });
      dispatch({ type: 'SET_LOADING_NARRATIVES', payload: false });
      console.log('did we get here? CounternarrativeOptions:', formattedCounterNarratives)
    } catch (error) {
      console.error('Failed to identify weaknesses:', error);
      dispatch({ type: 'SET_LOADING_NEWS', payload: false });
    }
  };

  const fetchAndSetConclusion = async (selectedNarrative) => {
    try {
      console.log('starting conclusion context function');
      dispatch({ type: 'SET_LOADING_CONCLUSION', payload: true });
      const response = await conclusion({
        narrative: selectedNarrative.text,
        strategy: selectedNarrative.strategy
      });
      console.log("YAY CONCLUSION CONTENT", response);
      dispatch({
        type: 'SET_CONCLUSION_CONTENT',
        payload: response  // Directly setting the response object assuming it matches the expected structure.
      });
      dispatch({ type: 'SET_LOADING_CONCLUSION', payload: false });
    } catch (error) {
      console.error('Failed to conclude:', error);
      dispatch({ type: 'SET_LOADING_CONCLUSION', payload: false }); 
    }
  };

  return (
    <GameStateContext.Provider value={state}>
      <GameDispatchContext.Provider value={dispatch}>
        <GameFunctionContext.Provider value={{ fetchAndSetFacts, fetchAndSetEvents, fetchAndSetActors, fetchAndSetStrats, fetchAndSetCounterStrats, loginUser, setFactSelection, buildAndSetNarrative, selectNarrativeAndSetContent, selectEventAndSetContent, identifyWeaknessesAndSetContent, fetchAndSetConclusion, setCurrentPhase, setCurrentOutroView, setCurrentTurnPointView, setCurrentIntroView }}> 
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
