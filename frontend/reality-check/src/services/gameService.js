// src/services/gameService.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust based on your Flask API

export const fetchGameDetails = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/game/details`);
    return response.data;
  } catch (error) {
    console.error('Error fetching game details:', error);
    throw error;
  }
};

// Add more API functions as needed
