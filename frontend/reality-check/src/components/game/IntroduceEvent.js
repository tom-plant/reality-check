// IntroduceEvent.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './IntroduceEvent.css'; 

const IntroduceEvent = () => {
  const { eventNewsContent, isLoadingNews } = useGameState(); 
  const [content, setContent] = useState(null);

  // Initialize variables outside of the conditional scope
  let headline, story, imageUrl;
  
  // Render news content
  useEffect(() => {
    if (eventNewsContent && !isLoadingNews) {
      setContent(eventNewsContent.event_news_content);
    }
  }, [eventNewsContent, isLoadingNews]); 

  // Conditional destructuring of content
  if (!isLoadingNews && content) {
    headline = content.headline;
    story = content.story;
    imageUrl = content.image_url;
  }

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
