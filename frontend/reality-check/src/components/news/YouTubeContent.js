import React from 'react';
import './YouTubeContent.css'; 
import template from '../../assets/youtube.PNG';

const YouTubeContent = ({ thumbnail, description, isModal }) => {
  return (
    <div className={`youtube-content ${isModal ? 'modal' : ''}`}>
      <img src={template} alt="YouTube thumbnail template" className="background-image" />
      <img src={thumbnail} className="actual-thumbnail" />
      <p className="youtube-description">{description}</p>
    </div>
  );
};

export default YouTubeContent;
