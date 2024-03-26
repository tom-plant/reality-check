import React from 'react';

const EmailRecruitment = ({ setCurrentPhase }) => {
  return (
    <div className="email-recruitment">
      <h2>Email Recruitment</h2>
      <p>This is the Email Recruitment screen of the Intro phase. Here, players will be officially recruited and briefed for their mission.</p>
      <button onClick={() => setCurrentPhase('game')}>Start Main Game</button>
    </div>
  );
};

export default EmailRecruitment;