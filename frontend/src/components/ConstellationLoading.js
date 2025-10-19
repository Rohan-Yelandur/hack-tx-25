import React, { useEffect, useState, useRef } from 'react';
import './ConstellationLoading.css';

// Example constellation patterns (arrays of star positions)
const CONSTELLATIONS = [
  // Orion
  [
    { x: 20, y: 40 }, { x: 40, y: 60 }, { x: 60, y: 40 }, { x: 80, y: 60 },
    { x: 50, y: 80 }, { x: 30, y: 80 }, { x: 70, y: 80 }
  ],
  // Cassiopeia
  [
    { x: 10, y: 20 }, { x: 30, y: 30 }, { x: 50, y: 10 }, { x: 70, y: 30 }, { x: 90, y: 20 }
  ],
  // Big Dipper
  [
    { x: 15, y: 70 }, { x: 30, y: 60 }, { x: 45, y: 50 }, { x: 60, y: 40 },
    { x: 75, y: 30 }, { x: 90, y: 20 }, { x: 80, y: 60 }
  ],
  // Lyra
  [
    { x: 30, y: 30 }, { x: 50, y: 20 }, { x: 70, y: 30 }, { x: 60, y: 50 }, { x: 40, y: 50 }
  ],
  // Cygnus
  [
    { x: 50, y: 10 }, { x: 50, y: 30 }, { x: 50, y: 50 }, { x: 30, y: 70 }, { x: 70, y: 70 }
  ],
  // Scorpius
  [
    { x: 20, y: 80 }, { x: 35, y: 65 }, { x: 50, y: 50 }, { x: 65, y: 35 }, { x: 80, y: 20 }, { x: 60, y: 60 }, { x: 40, y: 80 }
  ]
];

const STAR_DELAY = 200; // ms between lighting up stars
const FADE_DELAY = 600; // ms to fade out constellation

export default function ConstellationLoading() {
  const [constellationIdx, setConstellationIdx] = useState(0);
  const [litStars, setLitStars] = useState(0);
  const [fading, setFading] = useState(false);
  const timeoutRef = useRef();

  useEffect(() => {
    if (fading) {
      timeoutRef.current = setTimeout(() => {
        setFading(false);
        setLitStars(0);
        setConstellationIdx(idx => (idx + 1) % CONSTELLATIONS.length);
      }, FADE_DELAY);
      return () => clearTimeout(timeoutRef.current);
    }
    if (litStars < CONSTELLATIONS[constellationIdx].length) {
      timeoutRef.current = setTimeout(() => {
        setLitStars(litStars + 1);
      }, STAR_DELAY);
    } else {
      timeoutRef.current = setTimeout(() => {
        setFading(true);
      }, FADE_DELAY);
    }
    return () => clearTimeout(timeoutRef.current);
  }, [litStars, fading, constellationIdx]);

  const stars = CONSTELLATIONS[constellationIdx];

  return (
    <div className={`constellation-loading${fading ? ' fading' : ''}`}>
      <svg viewBox="0 0 100 100" width="80" height="80">
        {stars.map((star, i) => (
          <circle
            key={i}
            cx={star.x}
            cy={star.y}
            r={litStars > i ? 4 : 2}
            fill={litStars > i ? '#8b7fd8' : '#222b44'}
            opacity={litStars > i ? 1 : 0.5}
            style={{ transition: 'all 0.3s' }}
          />
        ))}
        {/* Draw lines between lit stars */}
        {stars.map((star, i) => (
          i > 0 && litStars > i ? (
            <line
              key={`line-${i}`}
              x1={stars[i - 1].x}
              y1={stars[i - 1].y}
              x2={star.x}
              y2={star.y}
              stroke="#8b7fd8"
              strokeWidth="1.5"
              opacity={0.7}
              style={{ transition: 'all 0.3s' }}
            />
          ) : null
        ))}
      </svg>
      <div className="constellation-loading-text">Generating your video explanation...</div>
    </div>
  );
}
