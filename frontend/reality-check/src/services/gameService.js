// src/services/gameService.js
import axios from 'axios';

// const API_BASE_URL = 'http://localhost:5000'; // Adjust this to your actual Flask API URL
const API_BASE_URL = 'https://reality-check-game-f90e2fef9c33.herokuapp.com'; 



// Function to authenticate (register or login) the user
export const authenticateUser = async (username, email) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth`, {
      username,
      email,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // Ensure you're handling credentials like cookies if needed
    });

    // Handle successful authentication here (e.g., storing user_id or other relevant info)
    return response.data;
  } catch (error) {
    console.error('Error during user authentication:', error);
    throw error;
  }
};

// Function to fetch initial list of facts
export const getFacts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/game/get_facts`, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // If your backend requires cookies or session
    });
    return response.data; // This should return the list of facts from your backend
  } catch (error) {
    console.error('Error fetching facts:', error);
    throw error;
  }
};

// Function to fetch initial list of events
export const getEvents = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/game/get_events`, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // If your backend requires cookies or session
    });
    return response.data; // This should return the list of events from your backend
  } catch (error) {
    console.error('Error fetching events:', error);
    throw error;
  }
};

export const generateNarrativeFromFacts = async (selectedFactCombination) => {
  try {
    // Transform selectedFactCombination to an array of fact texts
    console.log(selectedFactCombination)
    const selectedFactsTexts = selectedFactCombination.map(fact => fact.text);
    const response = await axios.post(`${API_BASE_URL}/game/select_facts`, {
      selected_facts: selectedFactsTexts, // Send the transformed array
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error generating narrative from facts:', error.response ? error.response.data : error);
    throw error;
  }
};

// Function to select a narrative based on selected facts
export const selectNarrative = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_narrative`, {
      selected_narrative: selectedNarrative
    }, {
      withCredentials: true 
    });
    return response.data;
  } catch (error) {
    console.error('Error selecting narrative:', error);
    throw error;
  }
};

// Function to introduce an event and retrieve news content
export const introduceEvent = async (selectedEvent) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/introduce_event`, {
      Event: selectedEvent
    }, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    console.error('Error introducing event:', error);
    throw error;
  }
};

// API function to identify weaknesses in narratives
export const identifyWeaknesses = async (updatedFactCombination) => {
  try {
    // Transform newFactCombination to the required format 
    const updatedFactsTexts = updatedFactCombination.map(fact => fact.text);

    const response = await axios.post(`${API_BASE_URL}/game/identify_weaknesses`, {
      updated_fact_combination: updatedFactsTexts, 
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error identifying weaknesses in narrative:', error);
    throw error;
  }
};


// Function to save user progress
export const saveUserProgress = async (userProgress) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/save_progress`, {
      user_progress: userProgress,
    });
    return response.data;
  } catch (error) {
    console.error('Error saving user progress:', error);
    throw error;
  }
};

// Add more functions for other endpoints like fetchNarratives, fetchEventResponse, etc.
