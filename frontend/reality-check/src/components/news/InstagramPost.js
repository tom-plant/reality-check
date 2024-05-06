import React from 'react';
import './InstagramPost.css';
import template from '../../assets/instagram.PNG'

const InstagramPost = ({ text }) => {

    console.log('received text', text)

  return (
    <div className="instagram-post">
      <img src={template} alt="Instagram template" className="background-image" />
      <p className="instagram-text">{text}</p>
    </div>
  );
};

export default InstagramPost;


