import './App.css';
import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import VideoGenerator from './pages/VideoGenerator';
import Community from './pages/Community';
import Starfield from './components/Starfield';
import CelestialDecorations from './components/CelestialDecorations';
import ConstellationBackground from './components/ConstellationBackground';
import SplashScreen from './components/SplashScreen';
import { LessonProvider } from './context/LessonContext';
import About from './pages/About'

function AppContent() {
  const [showSplash, setShowSplash] = useState(true);
  const location = useLocation();

  useEffect(() => {
    // Only show splash on first load of home page
    if (location.pathname === '/' && showSplash) {
      const timer = setTimeout(() => {
        setShowSplash(false);
      }, 1000);

      return () => clearTimeout(timer);
    } else if (location.pathname !== '/') {
      // Hide splash immediately if not on home page
      setShowSplash(false);
    }
  }, [location.pathname, showSplash]);

  const shouldShowSplash = location.pathname === '/' && showSplash;

  return (
    <div className="App">
      <Starfield />
      <ConstellationBackground />
      <CelestialDecorations />
      
      <AnimatePresence mode="wait">
        {shouldShowSplash && (
          <SplashScreen key="splash" />
        )}
      </AnimatePresence>

      {!shouldShowSplash && <Header />}
      
      <main className="App-main">
        <Routes>
          <Route path="/" element={<VideoGenerator showSplash={shouldShowSplash} />} />
          <Route path="/community" element={<Community />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <LessonProvider>
        <AppContent />
      </LessonProvider>
    </Router>
  );
}

export default App;
