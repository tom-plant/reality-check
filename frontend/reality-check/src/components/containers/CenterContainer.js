import React from 'react';
import './CenterContainer.css'; // Import CSS

const CenterContainer = ({ children }) => {
  return (
    <div className="center-container">
      {children}
    </div>
  );
};

export default CenterContainer;
