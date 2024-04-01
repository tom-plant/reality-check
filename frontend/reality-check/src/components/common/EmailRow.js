import React from 'react';
import './EmailRow.css'; // Make sure the path is correct

const EmailRow = ({ title, subject, description, time, onClick }) => {
  return (
    <div className={`email-row ${onClick ? 'clickable' : ''}`} onClick={onClick}>
      <div className="email-title">
        <h3>{title}</h3>
      </div>
      <div className="email-message">
        <h4>
          {subject} - <span className="email-description">{description}</span>
        </h4>
      </div>
      <div className="email-time">
        <p>{time}</p>
      </div>
    </div>
  );
};

export default EmailRow;