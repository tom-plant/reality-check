import React from 'react';
import './NewsArticle.css';  

const NewsArticle = ({ article, photo, isModal }) => {
  return (
    <div className={`news-article ${isModal ? 'modal' : ''}`}>
      <h1 className="headline">{article.headline}</h1>
      <div className="article-content">
        {photo && <img src={photo} alt="News Visual" className="news-photo" />}
        <p className="body-text">{article.body}</p>
      </div>
    </div>
  );
};

export default NewsArticle;
