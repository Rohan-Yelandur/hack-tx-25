import './App.css';
import Header from './components/Header';
import VideoGenerator from './pages/VideoGenerator';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="App-main">
        <VideoGenerator />
      </main>
    </div>
  );
}

export default App;
