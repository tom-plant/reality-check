// UpdatedNarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './UpdatedNarrativeImpact.css'; 

const UpdatedNarrativeImpact = () => {
  const { secondaryNewsContent, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);

  // Initialize variables outside of the conditional scope
  let headline, story, imageUrl;

  // Render news content from the backend
  useEffect(() => {
    if (secondaryNewsContent && !isLoadingNews) {
      setContent(secondaryNewsContent.secondary_news_content);
    }
  }, [secondaryNewsContent, isLoadingNews]); 

  // Conditional destructuring of content
  if (!isLoadingNews && content) {
    headline = content.headline;
    story = content.story;
    imageUrl = content.image_url;
  }

  return (
    <div className="narrative-impact">
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

export default UpdatedNarrativeImpact;