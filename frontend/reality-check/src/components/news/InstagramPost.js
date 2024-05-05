import React from 'react';
import './InstagramPost.css';

const InstagramPost = ({ text }) => {

    console.log('received text', text)

  return (
    <div className="instagram-post">
      <img src="../../assets/instagram.png" alt="Instagram template" className="background-image" />
      <p className="instagram-text">{text}</p>
    </div>
  );
};

export default InstagramPost;
