import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameDispatch, useGameFunction } from '../../contexts/GameContext'; 
import './Alert.css'; 

const Alert = () => {
  const dispatch = useGameDispatch(); 
  const { setCurrentPhase } = useGameFunction();
  const { t } = useTranslation();
  const [currentPage, setCurrentPage] = useState(1);

  const handleNextClick = () => {
    setCurrentPage(2);
  };

  const handlePrevClick = () => {
    setCurrentPage(1);
  };

  const handleContinueClick = () => {
    setCurrentPhase('game'); 
    dispatch({ type: 'SET_CURRENT_VIEW', payload: 'IDENTIFY_WEAKNESSES' });
  };

  return (
    <div className="game-alert">
      <h2 className="alert-title">{t(`alert.${currentPage === 1 ? 'update.title' : 'pivot.title'}`)}</h2>
      <div className="alert-body">
        {currentPage === 1 ? (
          <>
            <p>{t('alert.update.spacer')}</p>
            <p>{t('alert.update.introduction')}</p>
            <p>{t('alert.update.challenge')}</p>
            <p>{t('alert.update.spacer')}</p>
          </>
        ) : (
          <>
            <p>{t('alert.update.response')}</p>
            <p>{t('alert.pivot.introduction')}</p>
            <p>{t('alert.pivot.task')}</p>
          </>
        )}
      </div>
      <div className="alert-navigation">
        <button onClick={handlePrevClick} disabled={currentPage === 1} className="alert-nav-button prev-button">{'<'}</button>
        {currentPage === 2 && <button onClick={handleContinueClick} className="continue-sim-button">{t('common.continue')}</button>}
        <button onClick={handleNextClick} disabled={currentPage === 2} className="alert-nav-button next-button">{'>'}</button>
      </div>
    </div>
  );
};

export default Alert;
