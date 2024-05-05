import React from 'react';
import './YouTubeContent.css'; 

const YouTubeContent = ({ thumbnail, description }) => {

console.log('received thumbnail', thumbnail)
console.log('received description', description)

  return (
    <div className="youtube-content">
      <img src="../../assets/youtube.png" alt="YouTube thumbnail template" className="background-image" />
      <img src={thumbnail} alt="Actual thumbnail" className="actual-thumbnail" />
      <p className="youtube-description">{description}</p>
    </div>
  );
};

export default YouTubeContent;
