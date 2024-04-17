import React, { useState } from 'react';
import { useTranslation } from 'react-i18next'; 
import { useGameState, useGameDispatch, useGameFunction } from '../../contexts/GameContext';
import ActorBox from '../ActorBox/ActorBox'; 
import './BuildNarrative.css'; 

const BuildNarrative = () => {
  const { t } = useTranslation();
  const { actors, selectedActor } = useGameState();

  return (
    <div className="build-narratives">
      <h2>{t('buildNarratives.title')}</h2>
      <div className="actors-list">
        {actors.map((actor) => (
          <ActorBox
            key={actor.id}
            actor={actor.text}
            isSelected={actor === selectedActor}
            disabled={selectedActor && actor !== selectedActor}
          />
        ))}
      </div>
    </div>
  );
};

export default BuildNarrative;