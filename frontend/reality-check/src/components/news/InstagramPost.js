import React from 'react';
import './InstagramPost.css';

const InstagramPost = ({ text, template, isModal }) => {
  return (
    <div className={`instagram-post ${isModal ? 'modal' : ''}`}>
      <img src={template} alt="Instagram template" className="background-image" />
      <p className="instagram-text">{text}</p>
    </div>
  );
};

export default InstagramPost;
