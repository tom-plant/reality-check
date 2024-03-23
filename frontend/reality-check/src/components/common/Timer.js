import React, { useState, useEffect, useRef } from 'react';
import './Timer.css';

const Timer = ({ onTimeUp }) => {
  const [seconds, setSeconds] = useState(5);
  const secondsRef = useRef(seconds); // Use a ref to keep track of the current seconds
  const intervalIdRef = useRef(null); // Use a ref to store the interval ID

  useEffect(() => {
    secondsRef.current = seconds; // Update the ref's value whenever seconds state changes
  }, [seconds]);

  useEffect(() => {
    const decrementSeconds = () => {
      setSeconds((currentSeconds) => {
        if (currentSeconds <= 1) {
          clearInterval(intervalIdRef.current); // Clear interval when countdown finishes
          onTimeUp(); // Call the onTimeUp callback
          return 0;
        } else {
          return currentSeconds - 1; // Continue countdown
        }
      });
    };

    intervalIdRef.current = setInterval(decrementSeconds, 1000);

    return () => clearInterval(intervalIdRef.current); // Cleanup interval on component unmount
  }, []); // Empty dependency array to ensure this effect only runs once on mount

  return (
    <div className={`timer ${seconds <= 10 ? 'warning' : ''}`}>
      {Math.floor(seconds / 60)}:{seconds % 60 < 10 ? `0${seconds % 60}` : seconds % 60}
    </div>
  );
};

export default Timer;
