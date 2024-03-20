// EventBox.js
import React from 'react';
import './EventBox.css'; 

const EventBox = ({ event, isSelected, container }) => {
  return (
    <div className={`event-box ${isSelected ? 'selected' : ''} ${container}`}>
      {event.text}
    </div>
  );
};

export default EventBox;
