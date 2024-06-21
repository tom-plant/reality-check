// UpdatedNarrativeImpact.js

import React, { useState } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import NarrativeBox from '../common/NarrativeBox';
import LoadingIcon from '../common/LoadingIcon';
import './UpdatedNarrativeImpact.css';

const UpdatedNarrativeImpact = () => {
  const { counterNarrativeOptions, isLoadingNarratives, selectedCounterNarrative } = useGameState();
  const dispatch = useGameDispatch();
  const { fetchAndSetConclusion, setCurrentPhase } = useGameFunction();
  const [buttonClicked, setButtonClicked] = useState(false);

  // Handle narrative selection
  const handleNarrativeConfirmation = () => {
    if (!buttonClicked && selectedCounterNarrative) {
      setButtonClicked(true);
      dispatch({ type: 'SET_SECONDARY_NARRATIVE_CONTENT', payload: selectedCounterNarrative }); 
      fetchAndSetConclusion(selectedCounterNarrative);
      setCurrentPhase('outro'); 
      dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'CONCLUSION_WRAP_UP' });
      dispatch({ type: 'TOGGLE_OUTRO_POPUP' });
    }
  };

  return (
    <div className="updated-narrative-impact">
      {isLoadingNarratives ? (
        <div className="loading-container">
          <LoadingIcon />
        </div>
      ) : (
        <>
          <h2>Counternarrative Options</h2>
          <div className="narratives-list">
            {counterNarrativeOptions && counterNarrativeOptions.map((narrative) => (
              <NarrativeBox 
                key={narrative.id} 
                narrative={narrative}
                isSelected={selectedCounterNarrative && narrative === selectedCounterNarrative}
                container="left"
              />
            ))}
          </div>
          <button
            className="confirm-narrative"
            disabled={!selectedCounterNarrative}
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