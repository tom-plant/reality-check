// SelectedNarrative.js

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import NarrativeBox from '../common/NarrativeBox'; 
import LoadingIcon from '../common/LoadingIcon';
import './SelectNarratives.css'; 

const SelectNarratives = () => {
  const { narrativeOptions, selectedNarrative, isLoadingNarratives } = useGameState();
  const { selectNarrativeAndSetContent } = useGameFunction(); 
  const [buttonClicked, setButtonClicked] = useState(false); 
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  // Generate news content upon narrative selection
  const handleNarrativeConfirmation = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      selectNarrativeAndSetContent(selectedNarrative);
      dispatch({ type: 'SET_CURRENT_VIEW', payload: 'NARRATIVE_IMPACT' }); 
    }
  };

  return (
    <div className="select-narratives">
      {isLoadingNarratives ? (
        <div className="loading-container">
          <LoadingIcon />
        </div>
      ) : (
        <>
          <h2>{t('selectNarratives.title')}</h2>
          <div className="narratives-list">
            {narrativeOptions && narrativeOptions.map((narrative) => (
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
            {t('common.promoteNarrative')}
          </button>
        </>
      )}
    </div>
  );
};

export default SelectNarratives;


