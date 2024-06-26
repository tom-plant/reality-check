import React from 'react';
import { useGameState, useGameFunction } from '../../contexts/GameContext';
import AuthLogin from '../game/AuthLogin';  
import ExpoInbox from '../game/ExpoInbox'; 
import EmailRecruitment from '../game/EmailRecruitment';  
import CenterContainer from '../containers/CenterContainer';
import GmailContainer from '../containers/GmailContainer'
import './IntroLayout.css'; 

const IntroLayout = () => {
  const { currentIntroView } = useGameState();
  const { setCurrentIntroView, setCurrentPhase } = useGameFunction();


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


  return (
    <div className="intro-layout">
      {currentIntroView === 'AUTH_LOGIN' ? (
        <CenterContainer>{renderIntroContent()}</CenterContainer>
      ) : (
        <GmailContainer>{renderIntroContent()}</GmailContainer>
      )}
    </div>
  );
};

export default IntroLayout;
