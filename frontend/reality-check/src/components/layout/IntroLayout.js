import React from 'react';
import { useGameState, useGameFunction, useGameDispatch } from '../../contexts/GameContext';
import AuthLogin from '../game/AuthLogin';  
import ExpoInbox from '../game/ExpoInbox'; 
import EmailRecruitment from '../game/EmailRecruitment';  
import CenterContainer from '../containers/CenterContainer';
import GmailContainer from '../containers/GmailContainer'
import EmailPopup from '../popups/EmailPopup';
import './IntroLayout.css'; 

const IntroLayout = () => {
  const { currentIntroView, isEmailPopupVisible } = useGameState();
  const { setCurrentIntroView, setCurrentPhase } = useGameFunction();
  const dispatch = useGameDispatch();


  const renderIntroContent = () => {
    switch (currentIntroView) {
      case 'AUTH_LOGIN':
        return <AuthLogin setCurrentIntroView={setCurrentIntroView} />;
      case 'EXPO_INBOX':
        return <ExpoInbox setCurrentIntroView={setCurrentIntroView} />;
      case 'EMAIL_RECRUITMENT':
        return <EmailRecruitment setCurrentPhase={setCurrentPhase} />;
      default:
        return <AuthLogin setCurrentIntroView={setCurrentIntroView} />;
    }
  };

  const closeEmailPopup = () => {
    dispatch({ type: 'TOGGLE_EMAIL_POPUP' });
  };

  return (
    <div className="intro-layout">
      {currentIntroView === 'AUTH_LOGIN' ? (
        <CenterContainer>{renderIntroContent()}</CenterContainer>
      ) : (
        <GmailContainer>{renderIntroContent()}</GmailContainer>
      )}
      {isEmailPopupVisible && (
        <EmailPopup onClose={closeEmailPopup} />
      )}
    </div>
  );
};

export default IntroLayout;
