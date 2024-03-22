// UpdatedNarrativeImpact.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext';


const UpdatedNarrativeImpact = () => {
  const { secondaryNewsContent, secondaryNarrative } = useGameState();
  console.log('secondaryNarrative from context:', secondaryNarrative);


  // Assuming primaryNewsContent has headline, story, and imageUrl properties
  const { headline, story, imageUrl } = secondaryNewsContent || {}; // Add a fallback to prevent errors if secondaryNewsContent is undefined

  return (
    <div className="narrative-impact">
      <h1>{headline}</h1>
      {imageUrl && <img src={imageUrl} alt="News Visual" />}
      <p>{story}</p>
    </div>
  );
};

export default UpdatedNarrativeImpact;