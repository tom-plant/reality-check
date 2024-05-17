import React from 'react';
import './CenterContainer.css'; // Import CSS
import { useGameState } from '../../contexts/GameContext'; // Adjust the path as needed

const CenterContainer = ({ children }) => {
  const { currentPhase } = useGameState(); // Assuming currentPhase is stored in this context

  // Determine the style based on the current phase
  const containerStyle = {
    position: 'absolute',
    width: '80%', // Adjust the width as needed
    height: '55%', // Adjust based on your layout
    top: '25%', // Adjust to position below the header
    boxSizing: 'border-box',
    borderRadius: '5px',
    backgroundColor: currentPhase === 'turn-point' ? 'none' : 'rgba(255, 255, 255, 0.2)' // Conditional border
  };

  return (
    <div className="center-container" style={containerStyle}>
      {children}
    </div>
  );
};

export default CenterContainer;
