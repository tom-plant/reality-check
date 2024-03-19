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
      {/* <div className="line line-1"></div>
      <div className="line line-2"></div>
      <div className="line line-3"></div>
      <div className="line line-4"></div>
      <div className="line line-5"></div> */}
    </div>
  );
};

export default DynamicBackground;
