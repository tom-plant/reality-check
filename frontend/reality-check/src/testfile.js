import React from 'react';
import { useTranslation } from 'react-i18next';

const TestComponent = () => {
  const { t } = useTranslation();

  return <div>{t('common.start')}</div>;
};

export default TestComponent;
