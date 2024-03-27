import React, { useState, useEffect } from 'react';
import EventBox from '../common/EventBox';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import './EventPopup.css';

const EventPopup = ({ onClose }) => {
  const { events } = useGameState(); 
  const { selectEventAndSetContent } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const [selectedEventIndex, setSelectedEventIndex] = useState(null);
  const [isCycling, setIsCycling] = useState(false);
  const [showCloseButton, setShowCloseButton] = useState(false);
  const [displayedEvents, setDisplayedEvents] = useState(events.slice(0, 3)); 

  // Initially load a random selection of 3 events
  useEffect(() => {
    setDisplayedEvents(getRandomEvents(events, 3));
  }, [events]);

  // Get a random selection of facts
  const getRandomEvents = (eventsArray, count) => {
      let shuffled = [...eventsArray].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    };
  
  // Hide the close button when cycling starts
  const startCyclingEvents = () => {
    setIsCycling(true);
    setShowCloseButton(false); 
    let index = 0;

    const cycle = setInterval(() => {
      setSelectedEventIndex(index % events.length);
      index++;
    }, 200); 

    // Stop cycling after 6-7 seconds and select an event
    setTimeout(() => {
      clearInterval(cycle); 
      setIsCycling(false);
      const finalIndex = Math.floor(Math.random() * events.length);
      setSelectedEventIndex(finalIndex);
      setShowCloseButton(true); 
      dispatch({ type: 'SELECT_EVENT', payload: events[finalIndex] });
      selectEventAndSetContent(events[finalIndex]); 
    }, 6500); 
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <div className="events-container">
          {displayedEvents.map((event, index) => (
            <EventBox
              key={event.id}
              event={event}
              isSelected={index === selectedEventIndex}
              container="popup"
            />
          ))}
        </div>
        <button
          className="randomize-event"
          onClick={startCyclingEvents}
          disabled={isCycling || selectedEventIndex !== null}
        >
          Randomize Event
        </button>
        {showCloseButton && (
          <button
            className="close-button"
            onClick={onClose}
          >
            X
          </button>
        )}
      </div>
    </div>
  );
};

export default EventPopup;
