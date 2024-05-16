import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useGameDispatch } from '../../contexts/GameContext';
import './IntroPopup.css';

const IntroPopup = () => {
  const dispatch = useGameDispatch();
  const [currentScreen, setCurrentScreen] = useState(0);
  const { t } = useTranslation();

  const screens = [
    'introPopup.instructions',
    'introPopup.briefing',
    'introPopup.selectFactsInstructions'
  ];

  const handleNext = () => {
    if (currentScreen < screens.length - 1) {
      setCurrentScreen(currentScreen + 1);
    }
  };

  const handlePrev = () => {
    if (currentScreen > 0) {
      setCurrentScreen(currentScreen - 1);
    }
  };

  const handleContinue = () => {
    dispatch({ type: 'TOGGLE_INTRO_POPUP' });
  };


  const renderScreenContent = (screenKey) => {
    const screenData = t(screenKey, { returnObjects: true });
    return (
      <div className="popup-text-content"> {/* Wrap the text content in its own div */}
        <h2>{screenData.title}</h2>
        <p>{screenData.introduction}</p>

        {screenKey === 'introPopup.instructions' && (
        <>
          <h3>{screenData.whatYouWillDoTitle}</h3>
          <p>{screenData.engageScenarios}</p>
          <p>{screenData.informedDecisionMaking}</p>
          <p>{screenData.criticalAnalysis}</p>
          <p>{screenData.conclusion}</p>
          <p><strong>{screenData.readyToBegin}</strong></p>
        </>
      )}

      {screenKey === 'introPopup.briefing' && (
        <>
          <p>{screenData.note}</p>
          <h3>{screenData.keyPointsTitle}</h3>
          <h4>{screenData.natureOfCrisis.title}</h4>
          <p>{screenData.natureOfCrisis.description}</p>
          <h4>{screenData.affectedAreas.title}</h4>
          <p>{screenData.affectedAreas.description}</p>
          <h4>{screenData.responseMeasures.title}</h4>
          <p>{screenData.responseMeasures.description}</p>
          <p>{screenData.conclusion}</p>
          <p><strong>{screenData.reminder}</strong></p>
        </>
      )}

      {screenKey === 'introPopup.selectFactsInstructions' && (
        <>
          <p>{screenData.steps.examine.title}: {screenData.steps.examine.description}</p>
          <p>{screenData.steps.selection.title}: {screenData.steps.selection.description}</p>
          <p>{screenData.steps.timely.title}: {screenData.steps.timely.description}</p>
          <p><strong>{screenData.impact}</strong></p>
        </>
      )}
      </div>
    );
  };


  return (
    <div className="popup-overlay">
      <div className="intro-popup-content">
        {renderScreenContent(screens[currentScreen])}
        <div className="button-container"> 
          {currentScreen > 0 && (
            <button className="prev-button" onClick={handlePrev}>
              {t('common.previous')}
            </button>
          )}
          {currentScreen < screens.length - 1 ? (
            <button className="next-button" onClick={handleNext}>
              {t('common.next')}
            </button>
          ) : (
            <button className="start-button" onClick={handleContinue}>
              {t('common.start')}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default IntroPopup;
