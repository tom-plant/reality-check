// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import translationENG from './locales/eng/translation.json'; 
import translationEST from './locales/est/translation.json'; 
import translationRUS from './locales/rus/translation.json'; 


const resources = {
  eng: {
    translation: translationENG
  },
  est: {
    translation: translationEST
  },
  rus: {
    translation: translationRUS
  }
};

i18n
  .use(initReactI18next) // Passes i18n down to react-i18next
  .init({
    resources,
    lng: "eng", // Default language
    fallbackLng: 'eng',
    keySeparator: false, // We do not use keys in form messages.welcome
    interpolation: {
      escapeValue: false // React already safes from XSS
    }
  });

export default i18n;
