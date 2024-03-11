// src/context/GameContext.js
import React, { createContext, useContext, useReducer } from 'react';

const GameStateContext = createContext();
const GameDispatchContext = createContext();

const gameReducer = (state, action) => {
  switch (action.type) {
    // Define different actions here, e.g., start game, set view, update score, etc.
    default:
      throw new Error(`Unknown action type: ${action.type}`);
  }
};

const GameProvider = ({ children }) => {
  const [state, dispatch] = useReducer(gameReducer, { /* Initial state here */ });

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
