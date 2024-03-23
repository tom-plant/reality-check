import React, { useEffect } from 'react';
import { getFacts } from '../services/gameService'; // Adjust the path as needed

const FactTestComponent = () => {
  useEffect(() => {
    const fetchData = async () => {
      try {
        const factsData = await getFacts();
        console.log(factsData); // Log the fetched facts to the console
      } catch (error) {
        console.error('Failed to fetch facts:', error);
      }
    };

    fetchData();
  }, []);

  return <div>Check the console for fetched facts.</div>;
};

export default FactTestComponent;
