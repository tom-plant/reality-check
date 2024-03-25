// NarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import './NarrativeImpact.css';

const NarrativeImpact = () => {
  const { primaryNewsContent, isLoadingNews } = useGameState();

  // Local state to ensure the component updates when primaryNewsContent changes
  const [content, setContent] = useState(null);

  useEffect(() => {
    console.log(primaryNewsContent)
    if (primaryNewsContent && !isLoadingNews) {
      // Update local state with the new content, ensuring we're accessing the nested 'news_content'
      setContent(primaryNewsContent.news_content);
    }
  }, [primaryNewsContent, isLoadingNews]); // Depend on isLoadingNews and primaryNewsContent

  // Conditional rendering based on isLoadingNews and content availability
  if (isLoadingNews || !content) {
    return <div>Loading news content...</div>; // or any other loading indicator
  }

  // Destructure with correct property names, using 'image_url' instead of 'imageUrl'
  const { headline, story, image_url: imageUrl } = content;

  return (
    <div className="narrative-impact">
      <h1>{headline}</h1>
      {imageUrl && <img src={imageUrl} alt="News Visual" />}
      <p>{story}</p>
    </div>
  );
};

export default NarrativeImpact;

