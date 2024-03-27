// UpdatedNarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import './UpdatedNarrativeImpact.css'; 

const UpdatedNarrativeImpact = () => {
  const { secondaryNewsContent, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);

  // Render news content from the backend
  useEffect(() => {
    if (secondaryNewsContent && !isLoadingNews) {
      setContent(secondaryNewsContent.secondary_news_content);
    }
  }, [secondaryNewsContent, isLoadingNews]); 

  // Loading Animation
  if (isLoadingNews || !content) {
    return <div>Loading news content...</div>; 
  }

  // Destructure with correct property names
  const { headline, story, image_url: imageUrl } = content;

  return (
    <div className="narrative-impact">
      <h1>{headline}</h1>
      {imageUrl && <img src={imageUrl} alt="News Visual" />}
      <p>{story}</p>
    </div>
  );
};

export default UpdatedNarrativeImpact;