import React from 'react';
import './LeftContainer.css'; // Import CSS

const LeftContainer = ({ children }) => {
  return (
    <div className="left-container">
      {children}
    </div>
  );
};

export default LeftContainer;
