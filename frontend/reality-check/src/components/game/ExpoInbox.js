import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next'; 
import gmailBackground from '../../assets/gmail_inbox.png';
import EmailRow from '../common/EmailRow'; 
import './ExpoInbox.css';


const ExpoInbox = ({ setCurrentIntroView }) => {
  const { t } = useTranslation();

  // Separate the new email from the initial list
  const newEmail = {
    id: 0, 
    title: 'The Civic Resilience Project', 
    subject: 'URGENT Participation Request: Crisis Simulation', 
    description: 'Dear Citizen, Your immediate participation is requested...', 
    time: '9:17 AM'
  };

  const initialEmails = [
    { id: 1, title: 'BBC Alerts', subject: 'EMERGENCY ALERT - Eirist Citizens Advised to Stay Home', description: 'Power substation attacks reported across major voting centers in Eirist... ', time: '9:04 AM' },
    { id: 2, title: 'ThinkCritically Newsletter', subject: 'Deciphering Fact from Fiction', description: "This Week's Guide to Critical News Analysis...", time: '8:43 AM' },
    { id: 3, title: 'Prime Minister\'s Office Update', subject: '* Public Safety Announcement *', description: 'Important Measures for City Residents...', time: '8:31 AM' },
    { id: 4, title: 'CyberGuard Tips', subject: 'Stay Safe from Crisis Scams', description: 'Protect Yourself Against Rising Cyber Threats...', time: '8:12 AM' },
    { id: 5, title: 'World Events Digest 🧠', subject: 'Understanding Global Impacts', description: 'How the Unfolding Crisis Affects Us All...', time: '7:41 AM' },
    { id: 6, title: 'Tech Trends', subject: 'Navigating Information Overload', description: 'Tools and Tips for Efficiently Managing News Intake...', time: '10:39 PM' },
    { id: 7, title: 'Amazon', subject: 'Your Order has Shipped!', description: 'Your order #123-456 has been shipped', time: '8:45 PM' },
    { id: 8, title: 'Local Heroes Feature', subject: 'Stories from the Local Emergency Providers', description: 'Meet the Brave Individuals Making a Difference...', time: '1:22 PM' },
    { id: 9, title: 'STEP Global Update', subject: ' !!! TRAVEL ADVISORIES !!!', description: 'Stay Informed on the Latest International Restrictions...', time: '11:14 AM' },
    { id: 10, title: 'PrizeBooster Daily', subject: 'Win Big Now! Exclusive Prize Just for You! 🌴', description: 'Claim Your Free Vacation to Paradise Island!', time: '8:14 AM' },
    { id: 11, title: 'DataSafe Notice', subject: 'Keeping Your Information Secure', description: 'Best Practices for Data Security in Uncertain Times...', time: '7:16 PM' },
    { id: 12, title: 'Coupon Counter', subject: 'Mega Deals Week - Unbelievable Discounts Inside!', description: 'Save Big on Electronics, Fashion, and More...', time: '9:35 PM' },
  ];
  
  // State to hold the combined list of emails
  const [combinedEmails, setCombinedEmails] = useState(initialEmails);

  useEffect(() => {
    // After a 5-second delay, add the new email to the top of the list
    const timer = setTimeout(() => {
      setCombinedEmails([newEmail, ...initialEmails]);
    }, 5000); // 5000ms delay

    // Cleanup the timer when the component unmounts
    return () => clearTimeout(timer);
  }, [initialEmails, newEmail]);

  
  return (
    <div className="expo-inbox" style={{ backgroundImage: `url(${gmailBackground})` }}>
      <div className="email-container">
        {combinedEmails.map(({ id, title, subject, description, time }, index) => (
          <EmailRow
            key={id}
            title={title}
            subject={subject}
            description={description}
            time={time}
            onClick={id === newEmail.id ? () => setCurrentIntroView('EMAIL_RECRUITMENT') : undefined}
            isNewEmail={id === newEmail.id} // Adds a new email indicator
          />
        ))}
      </div>
    </div>
  );
};


export default ExpoInbox;
