import React from 'react';
import { useGameState } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import './GameInstructions.css'

const GameInstructions = () => {
  const { currentView } = useGameState();
  const { t } = useTranslation();

  const getInstructionKeys = () => {
    switch (currentView) {
      case 'SELECT_FACTS':
        return;
      case 'SELECT_NARRATIVES':
        return [
          'selectNarratives.instructions.introduction'];
      case 'NARRATIVE_IMPACT':
        return [
          'narrativeImpact.introduction'];
      case 'INTRODUCE_EVENT':
        return [
        'introduceEvent.introduction'];
      case 'IDENTIFY_WEAKNESSES':
        return [
        'identifyWeaknesses.instructions.introduction'];
      case 'UPDATED_NARRATIVE_IMPACT':
        return [
          'updatedNarrativeImpact.instructions.introduction'];
      default:
        return; // Default instruction or null if none
    }
  };

  const instructionKeys = getInstructionKeys();

  // Return null if no instructions are needed for the current view
  if (!instructionKeys) return null;

  return (
    <div className="game-instructions">
      {instructionKeys.map((key) => (
        <p key={key}>{t(key)}</p> // Using the key as React key for each paragraph
      ))}
    </div>
  );
};

export default GameInstructions;
