// IntroduceEvent.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './IntroduceEvent.css'; 

const IntroduceEvent = () => {
  const { eventNewsContent, isLoadingNews } = useGameState(); 
  const [content, setContent] = useState(null);

  // Render news content
  useEffect(() => {
    if (eventNewsContent && !isLoadingNews) {
      setContent(eventNewsContent.event_news_content);
    }
  }, [eventNewsContent, isLoadingNews]); 

  // Destructure with correct property names
  const { headline, story, image_url: imageUrl } = content;

  return (
    <div className="introduce-event">
      {isLoadingNews ? (
        <div className="loading-container">
          <LoadingIcon />
        </div>
      ) : (
        <div className="news-content"> 
          <h1>{headline}</h1>
          {imageUrl && <img src={imageUrl} alt="News Visual" />}
          <p>{story}</p>
        </div>
      )}
    </div>
  );
};

export default IntroduceEvent;
