// NarrativeImpact.js

import React from 'react';
import { useGameState } from '../../contexts/GameContext';


const NarrativeImpact = () => {
  const { primaryNewsContent } = useGameState();

  // Assuming primaryNewsContent has headline, story, and imageUrl properties
  const { headline, story, imageUrl } = primaryNewsContent || {}; // Add a fallback to prevent errors if primaryNewsContent is undefined

  return (
    <div className="narrative-impact">
      <h1>{headline}</h1>
      {imageUrl && <img src={imageUrl} alt="News Visual" />}
      <p>{story}</p>
    </div>
  );
};

export default NarrativeImpact;