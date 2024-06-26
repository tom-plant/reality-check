import React from 'react';
import './InstagramPost.css';
import template1 from '../../assets/instagram1.PNG';
import template2 from '../../assets/instagram2.PNG';
import template3 from '../../assets/instagram3.PNG';
import template4 from '../../assets/instagram4.PNG';
import template5 from '../../assets/instagram5.PNG';
import template6 from '../../assets/instagram6.PNG';
import template7 from '../../assets/instagram7.PNG';

const templates = [template1, template2, template3, template4, template5, template6, template7];

const getRandomTemplate = () => {
  const randomIndex = Math.floor(Math.random() * templates.length);
  return templates[randomIndex];
};

const InstagramPost = ({ text, isModal }) => {
  const template = getRandomTemplate();
  return (
    <div className={`instagram-post ${isModal ? 'modal' : ''}`}>
      <img src={template} alt="Instagram template" className="background-image" />
      <p className="instagram-text">{text}</p>
    </div>
  );
};

export default InstagramPost;
