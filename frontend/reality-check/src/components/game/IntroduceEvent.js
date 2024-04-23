// IntroduceEvent.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './IntroduceEvent.css'; 

const IntroduceEvent = () => {
  const { eventNewsContent, isLoadingNews } = useGameState(); 
  const [content, setContent] = useState(null);

  
  useEffect(() => {
    // Update the effect to handle new JSON structure
    if (eventNewsContent && !isLoadingNews) {
      // Assuming eventNewsContent directly contains the news content
      setContent(eventNewsContent);
    }
  }, [eventNewsContent, isLoadingNews]); 

  return (
    <div className="introduce-event">
      {isLoadingNews ? (
        <div className="loading-container">
          <LoadingIcon />
        </div>
      ) : content ? (
        <div className="news-content">
          {/* Ensure content.event_outcome_text is not undefined before trying to render it */}
          <h1>{"How Your Narrative Ends"}</h1>
          <p>{content.event_outcome_text || "No event content available"}</p>
        </div>
      ) : null}
    </div>
  );
};

export default IntroduceEvent;