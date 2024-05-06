// NarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import NewsArticle from '../news/NewsArticle';
import InstagramPost from '../news/InstagramPost';
import ShortformContent from '../news/ShortformContent';
import YouTubeContent from '../news/YouTubeContent';
import './NarrativeImpact.css';

const NarrativeImpact = () => {
  const { primaryNewsContent, isLoadingNews } = useGameState();
  const [content, setContent] = useState(null);

  useEffect(() => {
    console.log('Primary News Content at useEffect:', primaryNewsContent);
    if (primaryNewsContent && !isLoadingNews) {
      // Check if primaryNewsContent is a string and parse it if necessary
      const contentToSet = typeof primaryNewsContent === 'string' ? JSON.parse(primaryNewsContent) : primaryNewsContent;
      console.log('Setting content:', contentToSet);
      setContent({
        news_article: contentToSet.news_article || {},
        news_photo: contentToSet.news_photo || '',
        instagram: contentToSet.instagram?.instagram || '',
        shortform: contentToSet.shortform?.shortform || '',
        youtube: contentToSet.youtube?.youtube || '',
        youtube_thumbnail: contentToSet.youtube_thumbnail || ''
      });
    }
  }, [primaryNewsContent, isLoadingNews]);

  useEffect(() => {
    console.log('Updated content state:', content);
    if (content) {
      console.log('content.news_article', content.news_article);
      console.log('content.news_photo', content.news_photo);
      console.log('content.instagram', content.instagram);
      console.log('content.shortform', content.shortform);
      console.log('content.youtube', content.youtube);
      console.log('content.youtube_thumbnail', content.youtube_thumbnail);
    }
  }, [content]); // This useEffect will log details after content state updates


  return (
    <div className="scrollable-container"> {/* Outer container for scrolling */}
      <div className="narrative-impact">
        {isLoadingNews ? (
          <div className="news-loading-container">
            <LoadingIcon />
          </div>
        ) : content && content.instagram && 
             content.shortform && 
             content.youtube && content.youtube_thumbnail ? (
          <>
            <NewsArticle article={content.news_article} photo={content.news_photo} />
            <InstagramPost text={content.instagram} />
            <ShortformContent content={content.shortform} />
            <YouTubeContent thumbnail={content.youtube_thumbnail} description={content.youtube} />
          </>
        ) : (
          <p>No content available or content is still loading...</p>
        )}
      </div>
    </div>
  );
};

export default NarrativeImpact;