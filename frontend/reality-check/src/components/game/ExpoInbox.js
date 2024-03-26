import React from 'react';

const ExpoInbox = ({ setCurrentIntroView }) => {
  return (
    <div className="expo-inbox">
      <h2>Exposition Inbox</h2>
      <p>This is where the player receives background information or the setup for the game.</p>
      <button onClick={() => setCurrentIntroView('EMAIL_RECRUITMENT')}>Proceed to Email Recruitment</button>
    </div>
  );
};

export default ExpoInbox;
