import './App.css';
import Header from './components/Header';
import VideoGenerator from './pages/VideoGenerator';
import Starfield from './components/Starfield';
import CelestialDecorations from './components/CelestialDecorations';

function App() {
  return (
    <div className="App">
      <Starfield />
      <CelestialDecorations />
      <Header />
      <main className="App-main">
        <VideoGenerator />
      </main>
    </div>
  );
}

export default App;
