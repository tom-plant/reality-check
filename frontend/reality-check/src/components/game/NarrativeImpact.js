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
  const { newsArticleContent, instagramContent, youtubeContent, shortformContent, selectedNarrative, isLoadingNews, contentError } = useGameState();
  const { selectNarrativeAndSetContent, selectNewsArticleContent, selectInstagramContent, selectYouTubeContent, selectShortformContent } = useGameFunction();
  const [content, setContent] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const dispatch = useGameDispatch();

  console.log('newsArticleContent', newsArticleContent)
  console.log('instagramContent', instagramContent)
  console.log('youtubeContent', youtubeContent)
  console.log('shortformContent', shortformContent)

  const handleRetry = async (contentType) => {
    dispatch({ type: 'SET_CONTENT_ERROR', payload: false });
    dispatch({ type: 'SET_LOADING_NEWS', payload: true });

    try {
      switch (contentType) {
        case 'news_article':
          await selectNewsArticleContent(selectedNarrative);
          break;
        case 'instagram':
          await selectInstagramContent(selectedNarrative);
          break;
        case 'youtube':
          await selectYouTubeContent(selectedNarrative);
          break;
        case 'shortform':
          await selectShortformContent(selectedNarrative);
          break;
        default:
          break;
      }
    } catch (error) {
      dispatch({ type: 'SET_CONTENT_ERROR', payload: true });
    }

    dispatch({ type: 'SET_LOADING_NEWS', payload: false });
  };

  const handleRefresh = () => {
    // window.location.reload();
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'INTRODUCE_EVENT' });
  };

  return (
    <div className="scrollable-container">
      <h1 className="news-feed-title">News Feed</h1>
      <div className="narrative-impact">
        {isLoadingNews ? (
          <div className="news-loading-container">
            <LoadingIcon />
            <p>Please wait for all news and social media content to generate. This may take up to a minute. Faster load times are in development.</p>
          </div>
        ) : contentError ? (
          <div className="news-loading-container">
            <p>An error occurred. Please try again.</p>
            <button onClick={() => handleRetry('news_article')}>Retry News Article</button>
            <button onClick={() => handleRetry('instagram')}>Retry Instagram</button>
            <button onClick={() => handleRetry('youtube')}>Retry YouTube</button>
            <button onClick={() => handleRetry('shortform')}>Retry Shortform</button>
            <button onClick={handleRefresh}>Refresh</button>
          </div>
        ) : (
          <>
            {newsArticleContent && (
              <NewsArticle
                article={newsArticleContent.news_article}
                photo={newsArticleContent.news_photo}
              />
            )}
            {instagramContent && instagramContent.instagram && (
              <InstagramPost text={instagramContent.instagram.instagram} />
            )}
            {youtubeContent && youtubeContent.youtube && (
              <YouTubeContent
                thumbnail={youtubeContent.youtube_thumbnail}
                description={youtubeContent.youtube.youtube}
              />
            )}
            {shortformContent && shortformContent.shortform && (
              <ShortformContent
                content={shortformContent.shortform.shortform}
                image={shortformContent.shortform_image}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default NarrativeImpact;