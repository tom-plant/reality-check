// src/services/gameApi.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust this to your actual Flask API URL

// Function to fetch initial list of facts
export const fetchInitialFacts = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_facts`);
    return response.data;
  } catch (error) {
    console.error('Error fetching initial facts:', error);
    throw error;
  }
};

// Function to select a narrative based on selected facts
export const selectNarrative = async (selectedNarrative, selectedFacts) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_narrative`, {
      selected_narrative: selectedNarrative,
      selected_facts: selectedFacts,
    });
    return response.data;
  } catch (error) {
    console.error('Error selecting narrative:', error);
    throw error;
  }
};

// Function to introduce a follow-up event
export const introduceEvent = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/introduce_event`);
    return response.data;
  } catch (error) {
    console.error('Error introducing event:', error);
    throw error;
  }
};

// Function to identify weaknesses in narratives
export const identifyWeaknesses = async (newFacts, narrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/identify_weaknesses`, {
      new_facts: newFacts,
      narrative: narrative,
    });
    return response.data;
  } catch (error) {
    console.error('Error identifying weaknesses:', error);
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
