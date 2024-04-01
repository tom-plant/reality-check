import React from 'react';
import { useTranslation } from 'react-i18next'; 
import gmailBackground from '../../assets/gmailui.png';
import './ExpoInbox.css';



const ExpoInbox = ({ setCurrentIntroView }) => {
  const { t } = useTranslation();

  return (
    <div className="expo-inbox" style={{ backgroundImage: `url(${gmailBackground})` }}>
      <div className="email-container">
        {/* Import and render EmailRow components here */}
      </div>
      <button onClick={() => setCurrentIntroView('EMAIL_RECRUITMENT')}>{t('common.next')}</button>
    </div>
  );
};


export default ExpoInbox;
