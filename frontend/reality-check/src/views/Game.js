// Game.js

import { useState } from 'react';
import { useEffect } from 'react';
import React from 'react';
import Header from '../components/Header/Header'; 
import './Game.css'; // Ensure this is imported
import DynamicBackground from '../components/DynamicBackground/DynamicBackground';
import { 
  register,
  fetchInitialFacts, 
  selectNarrative, 
  introduceEvent, 
  identifyWeaknesses, 
  saveUserProgress 
} from '../services/gameService';

const Game = () => {


   
  useEffect(() => {
    const authenticateAndFetchData = async () => {
      await register('your_username', 'your_email');  // Add error handling as needed
      // Now call fetchInitialFacts or any other function that requires authentication
      const facts = await fetchInitialFacts();
      console.log('Fetched Initial Facts:', facts);
    };
  
    authenticateAndFetchData();
  }, []);


  // useEffect(() => {
  //   const testAPI = async () => {
  //     try {
  //       await login('testUsername', 'testPassword');  // Replace with actual credentials
  //       const facts = await fetchInitialFacts();
  //       console.log('Fetched Initial Facts:', facts);
  //     } catch (error) {
  //       console.error('Error in API calls:', error);
  //     }
  //   };
  
  //   testAPI();
  // }, []);


  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const facts = await fetchInitialFacts();
  //       console.log('Fetched Initial Facts:', facts);
  //     } catch (error) {
  //       console.error('Error fetching initial facts:', error);
  //     }
  //   };
  
  //   fetchData();
  // }, []);
  

  // //calling all at once is just a placeholder for now
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       // Fetch Initial Facts
  //       const facts = await fetchInitialFacts();
  //       console.log('Fetched Initial Facts:', facts);
  
  //       // Dummy data for selected narrative and facts
  //       const selectedNarrative = 'Narrative 1';
  //       const selectedFacts = ['Fact 1', 'Fact 2'];
  
  //       // Select a narrative based on selected facts
  //       const narrativeResponse = await selectNarrative(selectedNarrative, selectedFacts);
  //       console.log('Narrative Response:', narrativeResponse);
  
  //       // Introduce a follow-up event
  //       const eventResponse = await introduceEvent();
  //       console.log('Event Response:', eventResponse);
  
  //       // Dummy data for new facts and narrative
  //       const newFacts = ['Fact 3', 'Fact 4'];
  //       const narrative = 'Narrative 2';
  
  //       // Identify weaknesses in narratives
  //       const weaknessesResponse = await identifyWeaknesses(newFacts, narrative);
  //       console.log('Weaknesses Response:', weaknessesResponse);
  
  //       // Dummy data for user progress
  //       const userProgress = { score: 100, level: 2 };
  
  //       // Save user progress
  //       const progressResponse = await saveUserProgress(userProgress);
  //       console.log('Progress Response:', progressResponse);
  
  //     } catch (error) {
  //       console.error('Error in API calls:', error);
  //     }
  //   };
  
  //   fetchData();
  // }, []);



  return (
    <div className="game">
      <Header /> 
      <div className="line line-1"></div>
      <div className="line line-2"></div>
      <div className="line line-3"></div>
      <div className="line line-4"></div>
      <div className="line line-5"></div>
      <DynamicBackground />
      <div className="container left-container">
        {/* Content for left container */}
      </div>
      <div className="container right-container">
        {/* Content for right container */}
      </div>
    </div>
  );
};




export default Game;
