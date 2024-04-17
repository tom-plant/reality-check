// UpdatedNarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './UpdatedNarrativeImpact.css'; 

const UpdatedNarrativeImpact = () => {
  const { secondaryNarrativeOptions, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);


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