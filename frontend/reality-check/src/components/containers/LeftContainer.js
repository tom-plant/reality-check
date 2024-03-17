import React from 'react';

const LeftContainer = ({ children }) => {
  return (
    <div className="left-container">
      {/* Pass-through children */}
      {children}
    </div>
  );
};

export default LeftContainer;
