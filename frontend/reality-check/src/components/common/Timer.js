import React, { useState, useEffect } from 'react';
import './Timer.css'; // Make sure to create a corresponding CSS file

const Timer = ({ onTimeUp }) => {
  const [seconds, setSeconds] = useState(5);

  useEffect(() => {
    if (seconds > 0) {
      const intervalId = setInterval(() => {
        setSeconds(seconds - 1);
      }, 1000);
      return () => clearInterval(intervalId);
    } else {
      onTimeUp();
    }
  }, [seconds, onTimeUp]);

  return (
    <div className={`timer ${seconds <= 10 ? 'warning' : ''}`}>
      {Math.floor(seconds / 60)}:{seconds % 60 < 10 ? `0${seconds % 60}` : seconds % 60}
    </div>
  );
};

export default Timer;
