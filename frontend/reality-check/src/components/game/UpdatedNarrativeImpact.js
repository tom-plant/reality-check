// UpdatedNarrativeImpact.js

import React, { useState } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import NarrativeBox from '../common/NarrativeBox';
import LoadingIcon from '../common/LoadingIcon';
import './UpdatedNarrativeImpact.css';

const UpdatedNarrativeImpact = () => {
  const { secondaryNarrativeOptions, isLoadingNarrative, selectedNarrative } = useGameState();
  const dispatch = useGameDispatch();
  const { fetchAndSetConclusion, setCurrentPhase } = useGameFunction();
  const [buttonClicked, setButtonClicked] = useState(false);

  // Handle narrative selection
  const handleNarrativeConfirmation = () => {
    if (!buttonClicked && selectedNarrative) {
      setButtonClicked(true);
      dispatch({ type: 'SET_SECONDARY_NARRATIVE_CONTENT', payload: selectedNarrative }); 
      fetchAndSetConclusion(selectedNarrative);
      setCurrentPhase('outro'); 
      dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'CONCLUSION_WRAP_UP' });
    }
  };

  return (
    <div className="narrative-impact">
      {isLoadingNarrative ? (
        <div className="loading-container">
          <LoadingIcon />
        </div>
      ) : (
        <>
          <h2>Impact of Updated Narratives</h2>
          <div className="narratives-list">
            {secondaryNarrativeOptions && secondaryNarrativeOptions.map((narrative) => (
              <NarrativeBox 
                key={narrative.id} 
                narrative={narrative}
                isSelected={selectedNarrative && narrative === selectedNarrative}
                container="left"
              />
            ))}
          </div>
          <button
            className="confirm-narrative"
            disabled={!selectedNarrative}
            onClick={handleNarrativeConfirmation}
          >
            Confirm Selection
          </button>
        </>
      )}
    </div>
  );
};

export default UpdatedNarrativeImpact;