// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import About from './views/About';
import Game from './views/Game';
import GameProvider from './contexts/GameContext';
import './App.css';

function App() {
  return (
    <GameProvider>
      <Router>
        <div className="App">
          <nav>
            <ul>
              {/* <li><Link to="/">Game</Link></li> */}
              {/* <li><Link to="/about">About</Link></li> */}
            </ul>
          </nav>

          <Routes>
            <Route path="/about" element={<About />} />
            <Route path="/" element={<Game />} />
          </Routes>
        </div>
      </Router>
    </GameProvider>
  );
}

export default App;
