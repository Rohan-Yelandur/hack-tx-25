import './CelestialDecorations.css';

function CelestialDecorations() {
  return (
    <div className="celestial-decorations">
      {/* Planet 1 - Top right */}
      <div className="planet planet-1">
        <div className="planet-surface"></div>
        <div className="planet-glow"></div>
      </div>

      {/* Planet 2 - Bottom left */}
      <div className="planet planet-2">
        <div className="planet-surface"></div>
        <div className="planet-glow"></div>
      </div>
    </div>
  );
}

export default CelestialDecorations;
