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
  const { newsArticleContent, instagramContent, youtubeContent, shortformContent, selectedNarrative, contentError } = useGameState();
  const { selectNarrativeAndSetContent, selectNewsArticleContent, selectInstagramContent, selectYouTubeContent, selectShortformContent } = useGameFunction();
  const [loadingStates, setLoadingStates] = useState({
    newsArticle: true,
    instagram: true,
    youtube: true,
    shortform: true,
  });
  const [retryCount, setRetryCount] = useState(0);
  const dispatch = useGameDispatch();

  const handleRetry = async (contentType) => {
    dispatch({ type: 'SET_CONTENT_ERROR', payload: false });

    try {
      switch (contentType) {
        case 'news_article':
          setLoadingStates((prevState) => ({ ...prevState, newsArticle: true }));
          await selectNewsArticleContent(selectedNarrative);
          break;
        case 'instagram':
          setLoadingStates((prevState) => ({ ...prevState, instagram: true }));
          await selectInstagramContent(selectedNarrative);
          break;
        case 'youtube':
          setLoadingStates((prevState) => ({ ...prevState, youtube: true }));
          await selectYouTubeContent(selectedNarrative);
          break;
        case 'shortform':
          setLoadingStates((prevState) => ({ ...prevState, shortform: true }));
          await selectShortformContent(selectedNarrative);
          break;
        default:
          break;
      }
    } catch (error) {
      dispatch({ type: 'SET_CONTENT_ERROR', payload: true });
    }

    setLoadingStates((prevState) => ({ ...prevState, [contentType]: false }));
  };

  const handleRefresh = () => {
    window.location.reload();
    // dispatch({ type: 'SET_CURRENT_VIEW', payload: 'INTRODUCE_EVENT' });
  };

  useEffect(() => {
    if (newsArticleContent) {
      setLoadingStates((prevState) => ({ ...prevState, newsArticle: false }));
    }
    if (instagramContent) {
      setLoadingStates((prevState) => ({ ...prevState, instagram: false }));
    }
    if (youtubeContent) {
      setLoadingStates((prevState) => ({ ...prevState, youtube: false }));
    }
    if (shortformContent) {
      setLoadingStates((prevState) => ({ ...prevState, shortform: false }));
    }
  }, [newsArticleContent, instagramContent, youtubeContent, shortformContent]);


  return (
    <div className="scrollable-container">
      <h1 className="news-feed-title">News Feed</h1>
      <div className="narrative-impact">
        {contentError ? (
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
            {loadingStates.newsArticle ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating news article...</p>
              </div>
            ) : (
              newsArticleContent && (
                <NewsArticle
                  article={newsArticleContent.news_article}
                  photo={newsArticleContent.news_photo}
                />
              )
            )}
            {loadingStates.instagram ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating Instagram post...</p>
              </div>
            ) : (
              instagramContent && instagramContent.instagram && (
                <InstagramPost text={instagramContent.instagram.instagram} />
              )
            )}
            {loadingStates.youtube ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating YouTube content...</p>
              </div>
            ) : (
              youtubeContent && youtubeContent.youtube && (
                <YouTubeContent
                  thumbnail={youtubeContent.youtube_thumbnail}
                  description={youtubeContent.youtube.youtube}
                />
              )
            )}
            {loadingStates.shortform ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating shortform content...</p>
              </div>
            ) : (
              shortformContent && shortformContent.shortform && (
                <ShortformContent
                  content={shortformContent.shortform.shortform}
                  image={shortformContent.shortform_image}
                />
              )
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default NarrativeImpact;