// ActorBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import './ActorBox.css'; 

const ActorBox = ({ actor, isSelected, disabled, container}) => {
  const dispatch = useGameDispatch();
  const { selectedActor } = useGameState(); // Access the selected facts from context

  const toggleActorSelection = () => {
    if (disabled) return; // Early return if interaction is disabled
  
    const actionType = isSelected ? 'DESELECT_ACTOR' : 'SELECT_ACTOR';
    dispatch({ type: actionType, payload: actor });
  };


  return (
    <div 
      className={`actor-box ${isSelected ? 'selected' : ''} ${container}`} 
      onClick={toggleActorSelection}
    >
      {actor.text}
    </div>
  );
};

export default ActorBox;