// NarrativeImpact.js

import React, { useEffect, useState } from 'react';
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import LoadingIcon from '../common/LoadingIcon';
import NewsArticle from '../news/NewsArticle';
import InstagramPost from '../news/InstagramPost';
import ShortformContent from '../news/ShortformContent';
import YouTubeContent from '../news/YouTubeContent';
import Modal from '../popups/Modal'; 
import './NarrativeImpact.css';

import template1 from '../../assets/instagram1.PNG';
import template2 from '../../assets/instagram2.PNG';
import template3 from '../../assets/instagram3.PNG';
import template4 from '../../assets/instagram4.PNG';
import template5 from '../../assets/instagram5.PNG';
import template6 from '../../assets/instagram6.PNG';
import template7 from '../../assets/instagram7.PNG';

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
  const [modalContent, setModalContent] = useState(null); 
  const [showModal, setShowModal] = useState(false);  
  const [instagramTemplate, setInstagramTemplate] = useState(null);
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

  const handleContentClick = (content) => {
    setModalContent(content);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setModalContent(null);
  };

  useEffect(() => {
    if (newsArticleContent) {
      setLoadingStates((prevState) => ({ ...prevState, newsArticle: false }));
    }
    if (instagramContent) {
      setLoadingStates((prevState) => ({ ...prevState, instagram: false }));
      if (!instagramTemplate) {
        setInstagramTemplate(getRandomTemplate());
      }
    }
    if (youtubeContent) {
      setLoadingStates((prevState) => ({ ...prevState, youtube: false }));
    }
    if (shortformContent) {
      setLoadingStates((prevState) => ({ ...prevState, shortform: false }));
    }
  }, [newsArticleContent, instagramContent, youtubeContent, shortformContent]);

  const templates = [template1, template2, template3, template4, template5, template6, template7];
  
  const getRandomTemplate = () => {
    const randomIndex = Math.floor(Math.random() * templates.length);
    return templates[randomIndex];
  };


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
                <div onClick={() => handleContentClick(
                  <NewsArticle
                    article={newsArticleContent.news_article}
                    photo={newsArticleContent.news_photo}
                    isModal={true}
                  />
                )}>
                  <NewsArticle
                    article={newsArticleContent.news_article}
                    photo={newsArticleContent.news_photo}
                    isModal={false}
                  />
                </div>
              )
            )}
            {loadingStates.instagram ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating Instagram post...</p>
              </div>
            ) : (
              instagramContent && instagramContent.instagram && (
                <div onClick={() => handleContentClick(
                  <InstagramPost text={instagramContent.instagram.instagram} template={instagramTemplate} isModal={true} />
                )}>
                  <InstagramPost text={instagramContent.instagram.instagram} template={instagramTemplate} isModal={false} />
                </div>
              )
            )}
            {loadingStates.youtube ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating YouTube content...</p>
              </div>
            ) : (
              youtubeContent && youtubeContent.youtube && (
                <div onClick={() => handleContentClick(
                  <YouTubeContent
                    thumbnail={youtubeContent.youtube_thumbnail}
                    description={youtubeContent.youtube.youtube}
                    isModal={true} 
                  />
                )}>
                  <YouTubeContent
                    thumbnail={youtubeContent.youtube_thumbnail}
                    description={youtubeContent.youtube.youtube}
                    isModal={false} 
                  />
                </div>
              )
            )}
            {loadingStates.shortform ? (
              <div className="news-loading-container">
                <LoadingIcon />
                <p>Generating shortform content...</p>
              </div>
            ) : (
              shortformContent && shortformContent.shortform && (
                <div onClick={() => handleContentClick(
                  <ShortformContent
                    content={shortformContent.shortform.shortform}
                    image={shortformContent.shortform_image}
                    isModal={true}
                  />
                )}>
                  <ShortformContent
                    content={shortformContent.shortform.shortform}
                    image={shortformContent.shortform_image}
                    isModal={false}
                  />
                </div>
              )
            )}
          </>
        )}
      </div>
      <Modal show={showModal} onClose={closeModal}>
        {modalContent}
      </Modal>
    </div>
  );
};

export default NarrativeImpact;