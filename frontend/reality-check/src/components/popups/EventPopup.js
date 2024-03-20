import React, { useState } from 'react';
import EventBox from '../common/EventBox';
import { useGameDispatch } from '../../contexts/GameContext'; // Adjust the import path as needed
import './EventPopup.css';

const EventPopup = ({ events, onClose }) => {
  const dispatch = useGameDispatch();
  const [selectedEventIndex, setSelectedEventIndex] = useState(null);
  const [isCycling, setIsCycling] = useState(false);
  const [showCloseButton, setShowCloseButton] = useState(false);

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
    }, 6500); // Adjust the duration of the cycling effect as needed
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <div className="events-container">
          {events.map((event, index) => (
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
