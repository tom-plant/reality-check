// src/services/gameService.js
import axios from 'axios';

// const API_BASE_URL = 'http://localhost:5000'; 
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

// Function to fetch initial list of events
export const getActors = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/game/get_actors`, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // If your backend requires cookies or session
    });
    return response.data; // This should return the list of events from your backend
  } catch (error) {
    console.error('Error fetching actors:', error);
    throw error;
  }
};

// Function to fetch initial list of events
export const getStrats = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/game/get_strats`, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // If your backend requires cookies or session
    });
    return response.data; // This should return the list of events from your backend
  } catch (error) {
    console.error('Error fetching strats:', error);
    throw error;
  }
};

// Function to fetch initial list of events
export const getCounterStrats = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/game/get_counterstrats`, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // If your backend requires cookies or session
    });
    return response.data; // This should return the list of events from your backend
  } catch (error) {
    console.error('Error fetching counterstrats:', error);
    throw error;
  }
};

export const setSelectedFacts = async (selectedFactCombination) => {
  try {
    // Transform selectedFactCombination to an array of fact texts
    const selectedFactsTexts = selectedFactCombination.map(fact => fact.text);
    await axios.post(`${API_BASE_URL}/game/select_facts`, {
      selected_facts: selectedFactsTexts, // Send the transformed array
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
    // No data is expected to return, function completes successfully without return
  } catch (error) {
    console.error('Error setting selected facts:', error.response ? error.response.data : error);
    throw error;
  }
};

// Build a narrative with selected actor and strategies
export const buildNarrative = async (selectedActor, selectedStrategies) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/build_narrative`, {
      selected_actor: selectedActor,
      selected_strategies: selectedStrategies,
    }, { withCredentials: true });
    return response.data;
  } catch (error) {
    console.error('Error building narrative:', error);
    throw error;
  }
};

// Function to select news article content
export const selectNewsArticleContent = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_news_article`, {
      narrative: selectedNarrative.text,
      strategy: selectedNarrative.strategy
    }, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error selecting news article content:', error);
    throw error;
  }
};

// Function to select Instagram content
export const selectInstagramContent = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_instagram`, {
      narrative: selectedNarrative.text,
      strategy: selectedNarrative.strategy
    }, {
      withCredentials: true,
    });
    return response.data
  } catch (error) {
    console.error('Error selecting Instagram content:', error);
    throw error;
  }
};

// Function to select YouTube content
export const selectYouTubeContent = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_youtube`, {
      narrative: selectedNarrative.text,
      strategy: selectedNarrative.strategy
    }, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error selecting YouTube content:', error);
    throw error;
  }
};

// Function to select shortform content
export const selectShortformContent = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/select_shortform`, {
      narrative: selectedNarrative.text,
      strategy: selectedNarrative.strategy
    }, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error selecting shortform content:', error);
    throw error;
  }
};

// Function to commit primary narrative content
export const setPrimaryContent = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/set_primary_content`, {
      narrative: selectedNarrative.text,
      strategy: selectedNarrative.strategy
    }, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error committing primary narrative content:', error);
    throw error;
  }
};


// Function to introduce an event and retrieve news content
export const introduceEvent = async (selectedEvent) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/introduce_event`, {
      event_details: selectedEvent
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
export const identifyWeaknesses = async (updatedFactCombination, selectedStrategies) => {
  try {
    const updatedFactsTexts = updatedFactCombination.map(fact => fact.text);
    const response = await axios.post(`${API_BASE_URL}/game/identify_weaknesses`, {
      updated_fact_combination: updatedFactsTexts,
      selected_strategies: selectedStrategies
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


// API function to fetch conclusion based on the selected narrative
export const conclusion = async (selectedNarrative) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/game/conclusion`, {
      narrative: selectedNarrative.narrative,
      strategy: selectedNarrative.strategy
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error concluding:', error);
    throw error;
  }
};





// Add more functions for other endpoints like fetchNarratives, fetchEventResponse, etc.
