// NarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import './NarrativeImpact.css';

const NarrativeImpact = () => {
  const { primaryNewsContent, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);

  
  useEffect(() => {
    if (primaryNewsContent && !isLoadingNews) {
      setContent(primaryNewsContent);
    }
  }, [primaryNewsContent, isLoadingNews]);

  return (
    <div className="narrative-impact">
      {isLoadingNews ? (
        <div className="loading-container">
          <LoadingIcon />
        </div>
      ) : content ? (
        <div className="news-content">
          <p>{content}</p>    
          {/* <h1>{content.news_article.headline}</h1>  {/* Access headline correctly */}
          {/* <p>{content.news_article.body}</p>       Access body correctly */}
          {/* {content.news_photo && <img src={content.news_photo} alt="News Visual" />} */} 
        </div>
      ) : null}
    </div>
  );
};

export default NarrativeImpact;

