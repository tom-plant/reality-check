// IntroduceEvent.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import './IntroduceEvent.css'; // Make sure to create a corresponding CSS file

const IntroduceEvent = () => {
  const { eventNewsContent, isLoadingNews, selectedEvent } = useGameState(); // Assuming eventNewsContent and selectedEvent are stored in your context
  const [content, setContent] = useState(null);

  useEffect(() => {
    console.log('selectedEvent is: ',selectedEvent)
    console.log('eventNewsContent is: ',eventNewsContent)
    console.log('isLoadingNews: ',isLoadingNews)
    if (eventNewsContent && !isLoadingNews) {
      // Update local state with the new content, ensuring we're accessing the nested 'news_content'
      setContent(eventNewsContent.event_news_content);
    }
  }, [eventNewsContent, isLoadingNews]); // Depend on isLoadingNews and primaryNewsContent

  // Conditional rendering based on isLoadingNews and content availability
  if (isLoadingNews || !content) {
    return <div>Loading news content...</div>; // or any other loading indicator
  }

  // Destructure with correct property names, using 'image_url' instead of 'imageUrl'
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
