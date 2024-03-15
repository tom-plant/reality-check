// DynamicBackground.js

import React from 'react';
import './DynamicBackground.css';
import skyImage from '../../assets/sky.jpg'; 
import cityImage from '../../assets/city.PNG'; 
import sunImage from '../../assets/sun.PNG'; 

console.log(skyImage, cityImage, sunImage);

const DynamicBackground = () => {
  return (
    <div className="dynamic-background">
      <img src={skyImage} alt="Sky" className="background-layer sky" />
      <img src={cityImage} alt="City" className="background-layer city" />
      <img src={sunImage} alt="Sun" className="background-layer sun" />
    </div>
  );
};

export default DynamicBackground;
