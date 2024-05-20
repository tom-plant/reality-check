import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useGameState, useGameFunction } from '../../contexts/GameContext';
import StratBox from '../common/StratBox';
import CounterStratBox from '../common/CounterStratBox';
import './MatchStrats.css';

const MatchStrats = () => {
  const { strats, counterstrats } = useGameState();
  const { t } = useTranslation();
  const [matches, setMatches] = useState({});
  const [selectedStrat, setSelectedStrat] = useState(null);

  const handleStratSelect = (strat) => {
    setSelectedStrat(strat);
  };

  const handleCounterStratSelect = (counterstrat) => {
    if (selectedStrat) {
      setMatches((prevMatches) => ({
        ...prevMatches,
        [selectedStrat.id]: counterstrat.id,
      }));
      setSelectedStrat(null);
    }
  };

  const handleMatchEdit = (stratId) => {
    setMatches((prevMatches) => {
      const newMatches = { ...prevMatches };
      delete newMatches[stratId];
      return newMatches;
    });
  };

  return (
    <div className="match-strats">
      <h2>{t('matchStrats.title')}</h2>
      <div className="strategies-section">
        {strats.map((strat) => (
          <StratBox
            key={strat.id}
            strat={strat}
            isSelected={selectedStrat === strat}
            onSelect={handleStratSelect}
            isMatched={matches[strat.id]}
          />
        ))}
      </div>
      <div className="counter-strategies-section">
        {counterstrats.map((counterstrat) => (
          <CounterStratBox
            key={counterstrat.id}
            counterstrat={counterstrat}
            isSelected={selectedStrat && matches[selectedStrat.id] === counterstrat.id}
            onSelect={handleCounterStratSelect}
            onEditMatch={handleMatchEdit}
          />
        ))}
      </div>
    </div>
  );
};

export default MatchStrats;
