// DynamicBackground.js

import React, { useEffect, useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import './DynamicBackground.css';
import sky1Image from '../../assets/sky.jpg'; 
import sky2Image from '../../assets/sky2.jpg'; 
import sky3Image from '../../assets/sky3.jpg'; 
import sky4Image from '../../assets/sky4.jpg'; 
import sky5Image from '../../assets/sky5.jpg'; 
import sunImage from '../../assets/sun.PNG'; 
import city1Image from '../../assets/city1.PNG'; 
import city2Image from '../../assets/city2.PNG'; 
import city3Image from '../../assets/city3.PNG'; 
import city4Image from '../../assets/city4.PNG'; 
import city5Image from '../../assets/city5.PNG'; 


const DynamicBackground = () => {
  const { currentView } = useGameState(); 
  const [background, setBackground] = useState(sky1Image);
  const [city, setCity] = useState(city1Image);
  const [sunStyle, setSunStyle] = useState({ top: '55%', opacity: 1 });

  useEffect(() => {
    switch (currentView) {
      case 'BUILD_NARRATIVE':
        setBackground(sky2Image);
        setCity(city2Image);
        setSunStyle({ top: '70%', left: '35%', filter: 'hue-rotate(30deg)', opacity: 0.8 });
        break;
      case 'SELECT_NARRATIVES':
        setBackground(sky3Image);
        setCity(city3Image);
        setSunStyle({ top: '88%', left: '32%', filter: 'hue-rotate(60deg)', opacity: 0 });
        break;
      case 'NARRATIVE_IMPACT':
        setBackground(sky4Image);
        setCity(city4Image);
        setSunStyle({ top: '100%', left: '30%', filter: 'hue-rotate(90deg)', opacity: 0 });
        break;
      case 'INTRODUCE_EVENT':
        setBackground(sky5Image);
        setCity(city5Image);
        setSunStyle({ top: '100%', left: '29%', filter: 'hue-rotate(120deg)', opacity: 0 });
        break;
      default:
        setBackground(sky1Image);
        setCity(city1Image);
        setSunStyle({ top: '55%', left: '40%', filter: 'none', opacity: 1 });
    }
  }, [currentView]);

  return (
    <div className="dynamic-background">
      <img src={background} alt="Sky" className="background-layer sky" />
      <img src={city} alt="City" className="background-layer city" />
      <img src={sunImage} alt="Sun" className="background-layer sun" style={sunStyle} />
    </div>
  );
};

export default DynamicBackground;