import React from 'react';
import { useGameDispatch } from '../../contexts/GameContext';
import './UpdatedNarrativePopup.css'; 

const UpdatedNarrativePopup = ({ secondaryNarrative }) => {
  const dispatch = useGameDispatch();

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' }); // This will toggle the popup visibility
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'UPDATED_NARRATIVE_IMPACT' }); // Progress to the next phase
  };

  return (
    // Use 'popup-overlay' class to cover the entire screen
    <div className="popup-overlay"> 
      <div className="popup-content"> 
        <h2>Your Updated Narrative</h2>
        <p>{secondaryNarrative || "Loading updated narrative..."}</p>
        <button
          className="continue-button"
          onClick={handleContinue}
          disabled={secondaryNarrative}
        >
          Continue
        </button>
      </div>
    </div>
  );
};

export default UpdatedNarrativePopup;