import React, { useEffect, useState } from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext';
import './UpdatedNarrativePopup.css'; 

const UpdatedNarrativePopup = () => {
  const { secondaryNarrative, isLoadingNews } = useGameState();
  const dispatch = useGameDispatch();
  const [content, setContent] = useState(null);

  // Set content from context
  useEffect(() => {
    if (secondaryNarrative) {
    setContent(secondaryNarrative);
    }
  }, [secondaryNarrative]); 

  // Loading animation
  if (isLoadingNews || !content) {
    return <div>Loading news content...</div>; 
  }

  // Toggle off popup and progress to next phase
  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' }); 
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'UPDATED_NARRATIVE_IMPACT' });
  };

  return (
    <div className="popup-overlay"> 
      <div className="popup-content"> 
        <h2>Your Updated Narrative</h2>
        <p>{secondaryNarrative.text}</p>
        <button
          className="continue-button"
          onClick={handleContinue}
          disabled={isLoadingNews}
        >
          Continue
        </button>
      </div>
    </div>
  );
};

export default UpdatedNarrativePopup;