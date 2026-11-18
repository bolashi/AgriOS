import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
import ur from './locales/ur.json'
import sd from './locales/sd.json'
i18n.use(initReactI18next).init({resources:{en:{translation:en},ur:{translation:ur},sd:{translation:sd}},lng:localStorage.getItem('agrios-language')||'en',fallbackLng:'en',interpolation:{escapeValue:false}})
export default i18n
