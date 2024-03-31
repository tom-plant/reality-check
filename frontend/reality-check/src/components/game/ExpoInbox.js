import React from 'react';
import { useTranslation } from 'react-i18next'; 

const ExpoInbox = ({ setCurrentIntroView }) => {
  const { t } = useTranslation();

  return (
    <div className="expo-inbox">
      <h2>Exposition Inbox</h2>
      <p>This is where the player receives background information or the setup for the game.</p>
      <button onClick={() => setCurrentIntroView('EMAIL_RECRUITMENT')}>{t('common.next')}</button>
    </div>
  );
};

export default ExpoInbox;
