import React, { useEffect, useState } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import StratBox from '../common/StratBox';
import CounterStratBox from '../common/CounterStratBox';
import './ReviseStrategy.css';

const effectivenessMappings = [
    ['strong', 'medium', 'weak', 'medium'],  // For Showing the Cause-and-Effect
    ['weak', 'strong', 'medium', 'medium'],  // For Instructing What to Believe
    ['medium', 'medium', 'strong', 'weak'],  // For Highlighting Danger
    ['medium', 'weak', 'medium', 'strong']   // For Appealing to Personal Beliefs
];

const ReviseStrategy = () => {
    const dispatch = useGameDispatch();
    const { strats, counterstrats, selectedNarrative, selectedCounterNarrative, selectedStrat, selectedCounterStrat, currentOutroView, updatedFactCombination, counterNarrativeOptions, conclusionContent } = useGameState();
    const [effectiveness, setEffectiveness] = useState('');
    const { fetchAndSetConclusion, identifyWeaknessesAndSetContent } = useGameFunction();
    const { t } = useTranslation();
    const [shouldProceed, setShouldProceed] = useState(false);
    const [isLoadingWeaknesses, setIsLoadingWeaknesses] = useState(false);

    useEffect(() => {
        if (currentOutroView === 'REVISE_STRATEGY') {
            console.log("Initial strats:", strats);
            console.log("Initial counterstrats:", counterstrats);
            console.log("Selected narrative strategy:", selectedNarrative.strategy);
            console.log("Selected counter-narrative strategy:", selectedCounterNarrative.strategy);

            const selectedStratObj = strats.find(s => s.text === selectedNarrative.strategy);
            const selectedCounterStratObj = counterstrats.find(cs => cs.text === selectedCounterNarrative.strategy);

            if (selectedStratObj && selectedCounterStratObj) {
                dispatch({ type: 'CLEAR_SELECTED_STRAT' });
                dispatch({ type: 'CLEAR_SELECTED_COUNTERSTRAT' });

                dispatch({ type: 'SELECT_STRAT', payload: selectedStratObj });
                dispatch({ type: 'SELECT_COUNTERSTRAT', payload: selectedCounterStratObj });

                updateEffectiveness(selectedStratObj, selectedCounterStratObj);
            } else {
                console.error("Selected strategy or counter-strategy not found in arrays");
            }
        }
    }, [currentOutroView]);

    useEffect(() => {
        if (selectedCounterStrat.length === 1) {
            const selectedStratObj = strats.find(s => s.text === selectedNarrative.strategy);
            if (selectedStratObj) {
                updateEffectiveness(selectedStratObj, selectedCounterStrat[0]);
            }
        }
    }, [selectedCounterStrat]);

    useEffect(() => {
        if (shouldProceed && !isLoadingWeaknesses && counterNarrativeOptions.length > 0) {
            setShouldProceed(false);
            // Change the view after counterNarrativeOptions has been updated
            dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'CONCLUSION_WRAP_UP' });

            // Set the first item from counterNarrativeOptions as the selected counter-narrative
            const firstCounterNarrative = counterNarrativeOptions[0];
            dispatch({ type: 'SELECT_COUNTERNARRATIVE', payload: firstCounterNarrative });
            console.log('SelectedCounterNarrative after is now', selectedCounterNarrative);
            console.log('and the above should match this: ', firstCounterNarrative);

            // Fetch updated conclusion
            fetchAndSetConclusion(firstCounterNarrative);
        }
    }, [shouldProceed, isLoadingWeaknesses, counterNarrativeOptions, dispatch, fetchAndSetConclusion, selectedCounterNarrative]);

    const updateEffectiveness = (strat, counterstrat) => {
        console.log("Updating effectiveness for strat:", strat, "and counterstrat:", counterstrat);

        const stratIndex = strats.findIndex(s => s.id === strat.id);
        const counterStratIndex = counterstrats.findIndex(cs => cs.id === counterstrat.id);

        console.log("Strat index:", stratIndex);
        console.log("CounterStrat index:", counterStratIndex);

        if (stratIndex !== -1 && counterStratIndex !== -1) {
            setEffectiveness(effectivenessMappings[stratIndex][counterStratIndex]);
        } else {
            console.error("Strat or CounterStrat not found in arrays");
        }
    };

    const getOutcomeText = (effectiveness) => {
        switch (effectiveness.toLowerCase()) {
            case 'strong':
                return t('Peace');
            case 'medium':
                return t('Resolution');
            case 'weak':
                return t('Chaos');
            default:
                return t('Loading');
        }
    };

    const handleProceedClick = async () => {
        dispatch({ type: 'CLEAR_CONCLUSION_CONTENT' });
        dispatch({ type: 'CLEAR_COUNTERNARRATIVE_OPTIONS' });

        if (effectiveness === 'strong') {
            setIsLoadingWeaknesses(true);
            try {
                // Fetch new narrative content based on the updated strategy and counter-strategy
                console.log('right before identifyWeaknesses, selectedCounterStrat is', selectedCounterStrat);
                console.log('CounterNarrativeOptions before, which should be clear:', counterNarrativeOptions);
                await identifyWeaknessesAndSetContent(updatedFactCombination, selectedCounterStrat);
                console.log('CounterNarrativeOptions after:', counterNarrativeOptions);
                setIsLoadingWeaknesses(false);
                setShouldProceed(true);
            } catch (error) {
                console.error("Failed to proceed:", error);
                setIsLoadingWeaknesses(false);
            }
        }
    };

    return (
        <div className="revise-strategies">
            <div className="outcome-box">
                <span>Election Outcome: </span>
                <span className="outcome-value">{getOutcomeText(effectiveness)}</span>
            </div>
            <div className="effectiveness-bar">
                <div className={`segment red ${['weak', 'medium', 'strong'].includes(effectiveness) ? 'filled' : ''}`} />
                <div className={`segment yellow ${['medium', 'strong'].includes(effectiveness) ? 'filled' : ''}`} />
                <div className={`segment green ${effectiveness === 'strong' ? 'filled' : ''}`} />
            </div>
            <div className="effectiveness-text">
                {getOutcomeText(effectiveness)}
            </div>
            <div className="strategy-container">
                <div className="strategies-section">
                    {strats.map((strat, idx) => (
                        <StratBox
                            key={idx}
                            strat={strat}
                            isSelected={selectedStrat.includes(strat)}
                            disabled
                            container="match"
                        />
                    ))}
                </div>
                <div className="counter-strategies-section">
                    {counterstrats.map((counterstrat, idx) => (
                        <CounterStratBox
                            key={idx}
                            counterstrat={counterstrat}
                            isSelected={selectedCounterStrat.includes(counterstrat)}
                            container="match"
                            maxSelection={1}
                        />
                    ))}
                </div>
            </div>
            <div className="proceed-button-container">
                <button
                    className="proceed-button"
                    onClick={handleProceedClick}
                    disabled={effectiveness !== 'strong'}
                >
                    {t('Proceed')}
                </button>
            </div>
        </div>
    );
};

export default ReviseStrategy;
