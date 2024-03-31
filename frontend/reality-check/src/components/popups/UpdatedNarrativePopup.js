import React, { useEffect, useState } from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next'; 
import './UpdatedNarrativePopup.css'; 

const UpdatedNarrativePopup = () => {
  const { secondaryNarrative, isLoadingNews } = useGameState();
  const dispatch = useGameDispatch();
  const [content, setContent] = useState(null);
  const { t } = useTranslation();


  // Set content from context
  useEffect(() => {
    if (secondaryNarrative) {
    setContent(secondaryNarrative);
    }
  }, [secondaryNarrative]); 

  // Toggle off popup and progress to next phase
  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_UPDATED_NARRATIVE_POPUP' }); 
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'UPDATED_NARRATIVE_IMPACT' });
  };

  return (
    <div className="popup-overlay"> 
      <div className="popup-content"> 
        <h2>{t('common.updatedNarrative')}</h2>
        {isLoadingNews && <div>Loading news content...</div>}
        <p>{secondaryNarrative.text}</p>
        <button
          className="continue-button"
          onClick={handleContinue}
          disabled={isLoadingNews}
        >
          {t('common.continue')} 
        </button>
      </div>
    </div>
  );
};

export default UpdatedNarrativePopup;