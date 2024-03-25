import React, { useState, useEffect } from 'react';
import EventBox from '../common/EventBox';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import './EventPopup.css';

const EventPopup = ({ onClose }) => {
  const { events, selectedEvent, eventNewsContent } = useGameState(); 
  const { selectEventAndSetContent } = useGameFunction(); 
  const dispatch = useGameDispatch();
  const [selectedEventIndex, setSelectedEventIndex] = useState(null);
  const [isCycling, setIsCycling] = useState(false);
  const [showCloseButton, setShowCloseButton] = useState(false);
  const [displayedEvents, setDisplayedEvents] = useState(events.slice(0, 3)); // Start with the first 3 facts

  useEffect(() => {
    // Initially load a random selection of 3 events
    setDisplayedEvents(getRandomEvents(events, 3));
  }, [events]);

  const getRandomEvents = (eventsArray, count) => {
    // Get a random selection of facts
      let shuffled = [...eventsArray].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    };
  

  const startCyclingEvents = () => {
    setIsCycling(true);
    setShowCloseButton(false); // Hide the close button when cycling starts
    let index = 0;

    const cycle = setInterval(() => {
      setSelectedEventIndex(index % events.length);
      index++;
    }, 200); // Adjust the speed of cycling as needed

    // Stop cycling after 6-7 seconds and select an event
    setTimeout(() => {
      clearInterval(cycle); // Use the correct interval variable here
      setIsCycling(false);
      const finalIndex = Math.floor(Math.random() * events.length);
      setSelectedEventIndex(finalIndex);
      setShowCloseButton(true); // Show the close button after cycling stops

      // Dispatch the selected event to the context
      dispatch({ type: 'SELECT_EVENT', payload: events[finalIndex] });
      console.log('final index is:',events[finalIndex])
      selectEventAndSetContent(events[finalIndex]); // Pass the selected event directly
    }, 6500); // Adjust the duration of the cycling effect as needed
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
