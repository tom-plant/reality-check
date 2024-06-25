import React, { useState, useEffect, useRef } from 'react';
import { useGameState } from '../../contexts/GameContext'; 
import './Timer.css';

const Timer = ({ onTimeUp, startTimer }) => {
  const { introduceEventVisits } = useGameState(); 
  const [seconds, setSeconds] = useState(introduceEventVisits === 1 ? 2 : 4); // Set initial seconds based on introduceEventVisits
  const secondsRef = useRef(seconds); 
  const intervalIdRef = useRef(null); 

  useEffect(() => {
    secondsRef.current = seconds;
  }, [seconds]);

  // Decrement the seconds function
  useEffect(() => {
    const decrementSeconds = () => {
      setSeconds((currentSeconds) => {
        if (currentSeconds <= 1) {
          clearInterval(intervalIdRef.current); 
          onTimeUp();
          return 0;
        } else {
          return currentSeconds - 1; 
        }
      });
    };

    // If timer is started, decrement seconds
    if (startTimer) {
      intervalIdRef.current = setInterval(decrementSeconds, 1000);
    }

    // Cleanup function to clear the interval
    return () => clearInterval(intervalIdRef.current);
  }, [startTimer]); // Depend on the startTimer prop


  useEffect(() => {
    // Update the timer duration when introduceEventVisits changes
    if (introduceEventVisits === 1) {
      setSeconds(2);
    } else {
      setSeconds(4);
    }
  }, [introduceEventVisits]);

  return (
    <div className={`timer ${seconds <= 10 ? 'warning' : ''}`}>
      {Math.floor(seconds / 60)}:{seconds % 60 < 10 ? `0${seconds % 60}` : seconds % 60}
    </div>
  );
};

export default Timer;
