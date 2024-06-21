import React, { useEffect, useState } from 'react';
import { useGameDispatch, useGameState, useGameFunction } from '../../contexts/GameContext';
import { useTranslation } from 'react-i18next';
import StratBox from '../common/StratBox';
import CounterStratBox from '../common/CounterStratBox';
import './ReviseStrategy.css';

const effectivenessMappings = [
    ['strong', 'medium', 'weak', 'medium'],  // For Showing the Cause-and-Effect against counterstrats in order
    ['weak', 'strong', 'medium', 'medium'],  // For Instructing What to Believe against counterstrats in order
    ['medium', 'medium', 'strong', 'weak'],  // For Highlighting Danger against counterstrats in order
    ['medium', 'weak', 'medium', 'strong']   // For Appealing to Personal Beliefs against counterstrats in order
];

const ReviseStrategy = () => {
    const dispatch = useGameDispatch();
    const { strats, counterstrats, selectedNarrative, selectedCounterNarrative, selectedStrat, selectedCounterStrat, updatedFactCombination, counterNarrativeOptions, currentOutroView } = useGameState();
    const [effectiveness, setEffectiveness] = useState('');
    const { fetchAndSetConclusion, identifyWeaknessesAndSetContent } = useGameFunction();
    const { t } = useTranslation();
    const [shouldProceed, setShouldProceed] = useState(false);
    const [isLoadingWeaknesses, setIsLoadingWeaknesses] = useState(false);

    // UPON FIRST ARRIVING, we set the selectedStratObj and SelectedCoutnerStratObj to calculate local effectiveness. This should only run once I think. 
    useEffect(() => {
        if (currentOutroView === 'REVISE_STRATEGY') {

            const selectedStratObj = strats.find(s => s.text === selectedNarrative.strategy);
            const selectedCounterStratObj = counterstrats.find(cs => cs.text === selectedCounterNarrative.strategy);
    
            // console.log('UPON FIRST ARRIVIGNG We just set selectedStratObj and counterstratobj by taking our selected narratives strategy object and searching the strats values. here are those for reference:')
            // console.log('-------------STRATS INFO-------------')
            // console.log('selectedStratObj is:', selectedStratObj)
            // console.log('selectedNarrative is:', selectedNarrative)
            // console.log('strats is:', strats)
            // console.log('-------------COUNTERSTRATS INFO-------------')
            // console.log('selectedCounterStratObj is:', selectedCounterStratObj)
            // console.log('selectedCounterNarrative is:', selectedCounterNarrative)
            // console.log('counterstrats is:', counterstrats)
    
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

    // upon the player's changing selection of a counterstrat (bc that's the only one they can change), the local effectiveness state is updated
    useEffect(() => {
        if (selectedCounterStrat.length === 1) {
            const selectedStratObj = strats.find(s => s.text === selectedNarrative.strategy);
            if (selectedStratObj) {
                updateEffectiveness(selectedStratObj, selectedCounterStrat[0]);
            }
        }
    }, [selectedCounterStrat]);

    // 
    useEffect(() => {
        if (shouldProceed && !isLoadingWeaknesses && counterNarrativeOptions.length > 0) {
            setShouldProceed(false);
            // Change the view after counterNarrativeOptions has been updated
            dispatch({ type: 'SET_CURRENT_OUTRO_VIEW', payload: 'CONCLUSION_WRAP_UP' });

            // Set the first item from counterNarrativeOptions as the selected counter-narrative
            const firstCounterNarrative = counterNarrativeOptions[0];
            // console.log('what is being sent to the conclusion generator is this: ', firstCounterNarrative);
            dispatch({ type: 'SELECT_COUNTERNARRATIVE', payload: firstCounterNarrative });
            // console.log('SelectedCounterNarrative after is now', selectedCounterNarrative);
            // console.log('and the above should match this: ', firstCounterNarrative);

            // Fetch updated conclusion
            fetchAndSetConclusion(firstCounterNarrative);
        }
    }, [shouldProceed, isLoadingWeaknesses, counterNarrativeOptions, dispatch, fetchAndSetConclusion, selectedCounterNarrative]);

    // LOCAL effectiveness updater
    const updateEffectiveness = (strat, counterstrat) => {
        // console.log("Updating effectiveness for strat:", strat, "and counterstrat:", counterstrat);
        const stratIndex = strats.findIndex(s => s.id === strat.id);
        const counterStratIndex = counterstrats.findIndex(cs => cs.id === counterstrat.id);
        // console.log("Strat index:", stratIndex);
        // console.log("CounterStrat index:", counterStratIndex);

        if (stratIndex !== -1 && counterStratIndex !== -1) {
            setEffectiveness(effectivenessMappings[stratIndex][counterStratIndex]);
            // console.log('new effectiveness in the calculator is: ', effectiveness)
        } else {
            console.error("Strat or CounterStrat not found in arrays");
        }
    };

    // simple calculator to get outocme text from current matchup
    const getOutcomeText = (effectiveness) => {
        switch (effectiveness.toLowerCase()) {
            case 'strong':
                return t('common.peace');
            case 'medium':
                return t('common.resolution');
            case 'weak':
                return t('common.chaos');
            default:
                return t('common.loading');
        }
    };

    // Upon clicking proceed, clear old conclusion content
    const handleProceedClick = async () => {
        dispatch({ type: 'CLEAR_CONCLUSION_CONTENT' });
        dispatch({ type: 'CLEAR_COUNTERNARRATIVE_OPTIONS' });

        if (effectiveness === 'strong') {
            // console.log('effectivness is strong so were regenerating the conclusion')
            setIsLoadingWeaknesses(true);
            try {
                // Fetch new narrative content based on the updated strategy and counter-strategy
                // console.log('right before identifyWeaknesses call to generate new narrative, selectedCounterStrat is', selectedCounterStrat);
                // console.log('CounterNarrativeOptions before, which should be clear:', counterNarrativeOptions);
                // console.log('right before swtiching back, local effectivness is ', effectiveness)
                await identifyWeaknessesAndSetContent(updatedFactCombination, selectedCounterStrat);
                // console.log('CounterNarrativeOptions after:', counterNarrativeOptions);
                setIsLoadingWeaknesses(false);
                setShouldProceed(true);
            } catch (error) {
                // console.error("Failed to proceed:", error);
                setIsLoadingWeaknesses(false);
            }
        }
    };

    return (
        <div className="revise-strategies">
            <div className="outcome-box">
                <span>{t('conclusionWrapUp.electionOutcome')}</span>
                <span className="outcome-value">{getOutcomeText(effectiveness)}</span>
            </div>
            <div className="effectiveness-bar">
                <div className={`segment red ${['weak', 'medium', 'strong'].includes(effectiveness) ? 'filled' : ''}`} />
                <div className={`segment yellow ${['medium', 'strong'].includes(effectiveness) ? 'filled' : ''}`} />
                <div className={`segment green ${effectiveness === 'strong' ? 'filled' : ''}`} />
            </div>
            <div className="strategy-container">
                <div className="strategies-section">
                <h3>Narrative Strategy</h3>
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
                <h3>Counternarrative Strategy</h3>
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
                    {t('common.proceed')}
                </button>
            </div>
        </div>
    );
};

export default ReviseStrategy;

