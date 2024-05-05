// IdentifyWeaknesses.js

import React, { useState } from 'react';
import { useGameState } from '../../contexts/GameContext';
import FactBox from '../common/FactBox';
import { useTranslation } from 'react-i18next'; 
import './IdentifyWeaknesses.css'; 

const IdentifyWeaknesses = () => {
  const { facts, updatedFactCombination, timerHasEnded } = useGameState();
  const [displayedFacts, setDisplayedFacts] = useState(facts);  
  const { t } = useTranslation();


  return (
    <div className="identify-weaknesses">
      <h2>{t('selectFacts.title')}</h2>
      {displayedFacts.map(fact => (
        <FactBox
          key={fact.id}
          fact={fact}
          isSelected={updatedFactCombination.includes(fact)}
          disabled={timerHasEnded}
          container="left"
        />
      ))}
    </div>
  );
};

export default IdentifyWeaknesses;
