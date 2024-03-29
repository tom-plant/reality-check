// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import translationEN from './locales/en/translation.json'; 
import translationET from './locales/et/translation.json'; 
import translationRU from './locales/ru/translation.json'; 


const resources = {
  en: {
    translation: translationEN
  },
  et: {
    translation: translationET
  },
  ru: {
    translation: translationRU
  }
};

i18n
  .use(initReactI18next) 
  .init({
    resources: resources,
    debug: true, 
    lng: "en", 
    defaultNS: "translation", 
    fallbackLng: "en",
    interpolation: {
      escapeValue: false 
    }
  });


export default i18n;
