import React from 'react';
import './InstagramPost.css';
import template from '../../assets/instagram.PNG';

const InstagramPost = ({ text, isModal }) => {
  return (
    <div className={`instagram-post ${isModal ? 'modal' : ''}`}>
      <img src={template} alt="Instagram template" className="background-image" />
      <p className="instagram-text">{text}</p>
    </div>
  );
};

export default InstagramPost;
