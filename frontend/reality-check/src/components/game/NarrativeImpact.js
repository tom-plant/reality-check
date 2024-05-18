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
  const { primaryNewsContent, isLoadingNews, selectedNarrative, contentError } = useGameState();
  const { selectNarrativeAndSetContent } = useGameFunction();
  const [content, setContent] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const dispatch = useGameDispatch();
  
  useEffect(() => {
    console.log('Primary News Content at useEffect:', primaryNewsContent);
    if (primaryNewsContent && !isLoadingNews) {
      if (primaryNewsContent.error) {
        dispatch({ type: 'SET_CONTENT_ERROR', payload: true });
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
        dispatch({ type: 'SET_CONTENT_ERROR', payload: false });
      }
    }
  }, [primaryNewsContent, isLoadingNews, dispatch]);

  const handleRetry = async () => {
    setRetryCount((prevCount) => prevCount + 1);
    dispatch({ type: 'SET_CONTENT_ERROR', payload: false });
    dispatch({ type: 'SET_LOADING_NEWS', payload: true });
    await selectNarrativeAndSetContent(selectedNarrative);
  };

  const handleRefresh = () => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'INTRODUCE_EVENT' });
    // window.location.reload();
  };

  return (
    <div className="scrollable-container"> {/* Outer container for scrolling */}
      <h1 className="news-feed-title">News Feed</h1>
      <div className="narrative-impact">
        {isLoadingNews ? (
          <div className="news-loading-container">
            <LoadingIcon />
            <p>Please wait for all news and social media content to generate. This may take up to a minute. Faster load times are in development.</p>
          </div>
        ) : contentError ? (
          <div className="news-loading-container">
            {retryCount < 3 ? (
              <>
                <p>An error occurred. Please try again.</p>
                <button onClick={handleRetry}>Retry</button>
              </>
            ) : (
              <>
                <p>The problem is persisting. Please refresh to restart.</p>
                <button onClick={handleRefresh}>Refresh</button>
              </>
            )}
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