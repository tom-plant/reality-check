import React from 'react';

const NarrativeImpact = () => {
  return (
    <div>
      {/* Component content goes here */}
      <h2>Narrative Impact</h2>
    </div>
  );
};

export default NarrativeImpact;


//Within your game phase components (e.g., SelectFacts, SelectNarratives), 
// use the passed goToNextPhase function to transition to the next phase upon certain actions, 
// like selecting a fact or confirming a narrative.