import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import ActorBox from '../common/ActorBox'; 
import './BuildNarrative.css'; 

const BuildNarrative = () => {
  const { t } = useTranslation();
  const { actors, selectedActor } = useGameState();

  return (
    <div className="build-narratives">
      <h2>{t('buildNarratives.title')}</h2>
      <div className="actors-list">
        {actors && actors.map((actor) => (
          <ActorBox
            key={actor.id}
            actor={actor}
            isSelected={actor === selectedActor}
          />
        ))}
      </div>
    </div>
  );
};

export default BuildNarrative;