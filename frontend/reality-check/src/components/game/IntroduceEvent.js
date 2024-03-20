import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import './IntroduceEvent.css'; // Make sure to create a corresponding CSS file

const IntroduceEvent = () => {
  const { eventNewsContent, selectedEvent } = useGameState(); // Assuming eventNewsContent and selectedEvent are stored in your context

  // Destructure the necessary properties, providing fallbacks to handle undefined cases
  const { headline, story, imageUrl } = eventNewsContent || { headline: '', story: '', imageUrl: '' };

  // Check if the content is still loading and an event has been selected
  const isLoading = (!headline && !story && !imageUrl) && selectedEvent !== null;

  return (
    <div className="introduce-event">
      {isLoading ? (
        <p>Generating potential outcomes if this narrative takes hold and this event occurs…</p>
      ) : (
        <>
          <h1>{headline}</h1>
          {imageUrl && <img src={imageUrl} alt="Event Visual" className="event-image" />}
          <p>{story}</p>
        </>
      )}
    </div>
  );
};

export default IntroduceEvent;
