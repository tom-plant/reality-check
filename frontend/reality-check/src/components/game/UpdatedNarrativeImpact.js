// UpdatedNarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import './UpdatedNarrativeImpact.css'; 

const UpdatedNarrativeImpact = () => {
  const { secondaryNewsContent, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);


  useEffect(() => {
    console.log('secondaryNewsContent is: ',secondaryNewsContent)
    console.log('isLoadingNews: ',isLoadingNews)
    if (secondaryNewsContent && !isLoadingNews) {
      // Update local state with the new content, ensuring we're accessing the nested 'news_content'
      setContent(secondaryNewsContent.secondary_news_content);
    }
  }, [secondaryNewsContent, isLoadingNews]); // Depend on isLoadingNews and primaryNewsContent

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

export default UpdatedNarrativeImpact;