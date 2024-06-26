// IdentifyWeaknessesDisplay.js

import React, { useState} from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import FactBox from '../common/FactBox'; 
import './IdentifyWeaknessesDisplay.css'; 

const IdentifyWeaknessesDisplay = () => {
  const { updatedFactCombination, selectedFactCombination } = useGameState();
  const { identifyWeaknessesAndSetContent } = useGameFunction(); 
  const [buttonClicked, setButtonClicked] = useState(false); 
  const dispatch = useGameDispatch();
  const { t } = useTranslation();

  // Check if the updated fact selection and the same as existing fact selection
  const arraysAreEqual = (arr1, arr2) => {
    if (arr1.length !== arr2.length) return false;
    for (let i = 0; i < arr1.length; i++) {
      if (arr1[i].text !== arr2[i].text) return false; 
    }
    return true;
  };  

  // Set updated facts and generate updated news content
  const handleUpdateNarrative = () => {
    if (!buttonClicked) { 
      setButtonClicked(true); 
      dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' }); // Toggle the popup first
      dispatch({ type: 'RESET_SELECTION_ENDED', payload: true });
      setTimeout(() => {
        dispatch({ type: 'UPDATE_FACTS', payload: updatedFactCombination });
        identifyWeaknessesAndSetContent(updatedFactCombination);
      }, 0); 
    }
  };

  return (
    <div className="identify-weaknesses-display">
      <div className="facts-list">
        {updatedFactCombination.map(fact => (
          <FactBox
            key={fact.id}
            fact={fact}
            isSelected={true}
            disabled={false}
            container="right"
          />
        ))}
      </div>
      <button
        className="update-narrative"
        onClick={handleUpdateNarrative}
        disabled={arraysAreEqual(updatedFactCombination, selectedFactCombination)}
      >
        {t('common.updateNarrative')} 
      </button>
    </div>
  );
};

export default IdentifyWeaknessesDisplay;
