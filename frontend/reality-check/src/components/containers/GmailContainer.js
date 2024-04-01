import React from 'react';
import './GmailContainer.css'; 

const GmailContainer = ({ children }) => {
  return (
    <div className="gmail-container">
      {children}
    </div>
  );
};

export default GmailContainer;
