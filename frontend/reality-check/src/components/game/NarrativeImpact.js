// NarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './NarrativeImpact.css';

const NarrativeImpact = () => {
  const { primaryNewsContent, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);

  // Render news content from the backend
  useEffect(() => {
    if (primaryNewsContent && !isLoadingNews) {
      setContent(primaryNewsContent.news_content);
    }
  }, [primaryNewsContent, isLoadingNews]); 

  // Destructure with correct property names
  const { headline, story, image_url: imageUrl } = content;

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

export default NarrativeImpact;

