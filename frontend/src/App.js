import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import VideoGenerator from './pages/VideoGenerator';
import Community from './pages/Community';
import Starfield from './components/Starfield';
import CelestialDecorations from './components/CelestialDecorations';
import ConstellationBackground from './components/ConstellationBackground';

function App() {
  return (
    <Router>
      <div className="App">
        <Starfield />
        <ConstellationBackground />
        <CelestialDecorations />
        <Header />
        <main className="App-main">
          <Routes>
            <Route path="/" element={<VideoGenerator />} />
            <Route path="/community" element={<Community />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
