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

      {/* Galaxy spiral */}
      <div className="galaxy galaxy-1">
        <div className="galaxy-core"></div>
        <div className="galaxy-spiral"></div>
      </div>

      {/* Distant stars cluster */}
      <div className="star-cluster cluster-1"></div>
      <div className="star-cluster cluster-2"></div>
    </div>
  );
}

export default CelestialDecorations;
