import React from 'react';
import './ShortformContent.css';
import template from '../../assets/shortform.PNG';

const ShortformContent = ({ content, image, isModal }) => {
  return (
    <div className={`shortform-content ${isModal ? 'modal' : ''}`}>
      <img src={template} alt="Shortform template" className="background-image" />
      {image && <img src={image} alt="Shortform Content" className="overlay-image" />}
      <p className="shortform-text">{content}</p>
    </div>
  );
};

export default ShortformContent;
