// NarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import NewsArticle from '../news/NewsArticle';
import InstagramPost from '../news/InstagramPost';
import ShortformContent from '../news/ShortformContent';
import YouTubeContent from '../news/YouTubeContent';
import './NarrativeImpact.css';

const NarrativeImpact = () => {
  const { primaryNewsContent, isLoadingNews, selectedNarrative } = useGameState();
  const { selectNarrativeAndSetContent } = useGameFunction();
  const [content, setContent] = useState(null);
  const [error, setError] = useState(false);
  const dispatch = useGameDispatch();
  
  useEffect(() => {
    console.log('Primary News Content at useEffect:', primaryNewsContent);
    if (primaryNewsContent && !isLoadingNews) {
      if (primaryNewsContent.error) {
        setError(true);
        setContent(null);
      } else {
        // Check if primaryNewsContent is a string and parse it if necessary
        const contentToSet = typeof primaryNewsContent === 'string' ? JSON.parse(primaryNewsContent) : primaryNewsContent;
        setContent({
          news_article: contentToSet.news_article || {},
          news_photo: contentToSet.news_photo || '',
          instagram: contentToSet.instagram?.instagram || '',
          shortform: contentToSet.shortform?.shortform || '',
          shortform_image: contentToSet.shortform_image || '',
          youtube: contentToSet.youtube?.youtube || '',
          youtube_thumbnail: contentToSet.youtube_thumbnail || ''
        });
        setError(false);
      }
    }
  }, [primaryNewsContent, isLoadingNews]);

  const handleRetry = async () => {
    setError(false);
    dispatch({ type: 'SET_LOADING_NEWS', payload: true });
    await selectNarrativeAndSetContent(selectedNarrative);
  };

  useEffect(() => {
    console.log('Updated content state:', content);
    if (content) {
      console.log('content.news_article', content.news_article);
      console.log('content.news_photo', content.news_photo);
      console.log('content.instagram', content.instagram);
      console.log('content.shortform', content.shortform);
      console.log('content.shortform_image', content.shortform_image);
      console.log('content.youtube', content.youtube);
      console.log('content.youtube_thumbnail', content.youtube_thumbnail);
    }
  }, [content]); // This useEffect will log details after content state updates


  return (
    <div className="scrollable-container"> {/* Outer container for scrolling */}
      <h1 className="news-feed-title">News Feed</h1>
      <div className="narrative-impact">
        {isLoadingNews ? (
          <div className="news-loading-container">
            <LoadingIcon />
            <p>Please wait for all news and social media content to generate. This may take up to a minute. Faster load times are in development.</p>
          </div>
        ) : error ? (
          <div className="news-loading-container">
            <p>An error occurred. Please try again.</p>
            <button onClick={handleRetry}>Retry</button>
          </div>
        ) : content && content.instagram && 
             content.shortform && 
             content.youtube && content.youtube_thumbnail ? (
          <>
            <NewsArticle article={content.news_article} photo={content.news_photo} />
            <InstagramPost text={content.instagram} />
            <YouTubeContent thumbnail={content.youtube_thumbnail} description={content.youtube} />
            <ShortformContent content={content.shortform} image={content.shortform_image} />
          </>
        ) : (
          <p>An error occured. Please refresh to try again.</p>
        )}
      </div>
    </div>
  );
};

export default NarrativeImpact;