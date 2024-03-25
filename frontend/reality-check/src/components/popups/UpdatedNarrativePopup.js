import React, { useEffect, useState } from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext';
import './UpdatedNarrativePopup.css'; 

const UpdatedNarrativePopup = () => {
  const { secondaryNarrative, isLoadingNews } = useGameState();
  const dispatch = useGameDispatch();
  const [content, setContent] = useState(null);

  console.log('secondaryNarrative from context:', secondaryNarrative);

  useEffect(() => {
    if (secondaryNarrative) {
    console.log('secondary narrative is:', secondaryNarrative)
    setContent(secondaryNarrative);
    }
  }, [secondaryNarrative]); 

  // Conditional rendering based on isLoadingNews and content availability
  if (isLoadingNews || !content) {
    return <div>Loading news content...</div>; // or any other loading indicator
  }

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' }); // This will toggle the popup visibility
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'UPDATED_NARRATIVE_IMPACT' }); // Progress to the next phase
  };

  return (
    // Use 'popup-overlay' class to cover the entire screen
    <div className="popup-overlay"> 
      <div className="popup-content"> 
        <h2>Your Updated Narrative</h2>
        <p>{secondaryNarrative.text}</p>
        <button
          className="continue-button"
          onClick={handleContinue}
          // disabled={!secondaryNarrative}
        >
          Continue
        </button>
      </div>
    </div>
  );
};

export default UpdatedNarrativePopup;