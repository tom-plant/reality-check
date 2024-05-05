import React from 'react';
import './ShortformContent.css';  

const ShortformContent = ({ content }) => {

    console.log('received content', content)

  return (
    <div className="shortform-content">
      <img src="../../assets/shortform.PNG" alt="Shortform template" className="background-image" />
      <p className="shortform-text">{content}</p>
    </div>
  );
};

export default ShortformContent;
