import React from 'react';
import './PublicSentimentGauge.css';

const PublicSentimentGauge = ({ strategy }) => {
  let gaugeClass = '';
  if (strategy.effectiveness === 'strong') gaugeClass = 'strong';
  if (strategy.effectiveness === 'medium') gaugeClass = 'medium';
  if (strategy.effectiveness === 'weak') gaugeClass = 'weak';

  return (
    <div className={`public-sentiment-gauge ${gaugeClass}`}>
      <span>{strategy.effectiveness}</span>
    </div>
  );
};

export default PublicSentimentGauge;
