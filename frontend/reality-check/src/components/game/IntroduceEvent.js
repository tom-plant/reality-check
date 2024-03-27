// IntroduceEvent.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
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

  // Loading animation
  if (isLoadingNews || !content) {
    return <div>Loading news content...</div>; 
  }

  // Destructure with correct property names
  const { headline, story, image_url: imageUrl } = content;

  return (
    <div className="introduce-event">
      <h1>{headline}</h1>
      {imageUrl && <img src={imageUrl} alt="News Visual" />}
      <p>{story}</p>
    </div>
  );
};

export default IntroduceEvent;
