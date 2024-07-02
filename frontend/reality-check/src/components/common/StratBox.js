// StratBox.js
import React from 'react';
import { useGameDispatch, useGameState } from '../../contexts/GameContext'; 
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css'; // Import SweetAlert2 styles
import './StratBox.css'; 

const StratBox = ({ strat, isSelected, disabled, container }) => {
  const dispatch = useGameDispatch();
  const { selectedStrat } = useGameState(); // Access the selected strategies from context

  const toggleStratSelection = () => {
    if (disabled) return; // Early return if interaction is disabled

    let actionType, stratLimitReached;

    actionType = isSelected ? 'DESELECT_STRAT' : 'SELECT_STRAT';
    stratLimitReached = !isSelected && selectedStrat.length >= 2;

    if (!stratLimitReached) {
      dispatch({ type: actionType, payload: strat });
    } else {
      Swal.fire({
        text: 'You can select a maximum of 2 strategies. To deselect a strategy, click it again.',
        icon: 'warning',
        confirmButtonText: 'OK'
      });
    }
  };

  return (
    <div 
      className={`strat-box ${isSelected ? 'selected' : ''} ${container}`} 
      onClick={toggleStratSelection}
    >
      {strat.text}
    </div>
  );
};

export default StratBox;