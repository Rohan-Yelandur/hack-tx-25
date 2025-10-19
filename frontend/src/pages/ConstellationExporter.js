import React, { useRef } from 'react';
import './ConstellationExporter.css';

// Same constellation patterns from ConstellationLoading
const CONSTELLATIONS = [
  {
    name: 'Orion',
    stars: [
      { x: 20, y: 40 }, { x: 40, y: 60 }, { x: 60, y: 40 }, { x: 80, y: 60 },
      { x: 50, y: 80 }, { x: 30, y: 80 }, { x: 70, y: 80 }
    ]
  },
  {
    name: 'Cassiopeia',
    stars: [
      { x: 10, y: 20 }, { x: 30, y: 30 }, { x: 50, y: 10 }, { x: 70, y: 30 }, { x: 90, y: 20 }
    ]
  },
  {
    name: 'Big Dipper',
    stars: [
      { x: 15, y: 70 }, { x: 30, y: 60 }, { x: 45, y: 50 }, { x: 60, y: 40 },
      { x: 75, y: 30 }, { x: 90, y: 20 }, { x: 80, y: 60 }
    ]
  },
  {
    name: 'Lyra',
    stars: [
      { x: 30, y: 30 }, { x: 50, y: 20 }, { x: 70, y: 30 }, { x: 60, y: 50 }, { x: 40, y: 50 }
    ]
  },
  {
    name: 'Cygnus',
    stars: [
      { x: 50, y: 10 }, { x: 50, y: 30 }, { x: 50, y: 50 }, { x: 30, y: 70 }, { x: 70, y: 70 }
    ]
  },
  {
    name: 'Scorpius',
    stars: [
      { x: 20, y: 80 }, { x: 35, y: 65 }, { x: 50, y: 50 }, { x: 65, y: 35 }, { x: 80, y: 20 }, { x: 60, y: 60 }, { x: 40, y: 80 }
    ]
  }
];

const ConstellationIcon = ({ constellation, size = 512 }) => {
  const svgRef = useRef();

  const downloadSVG = () => {
    const svgElement = svgRef.current;
    const svgData = new XMLSerializer().serializeToString(svgElement);
    const blob = new Blob([svgData], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `constellation-${constellation.name.toLowerCase().replace(/\s+/g, '-')}.svg`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadPNG = () => {
    const svgElement = svgRef.current;
    const svgData = new XMLSerializer().serializeToString(svgElement);
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');
    
    const img = new Image();
    const blob = new Blob([svgData], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    
    img.onload = () => {
      ctx.drawImage(img, 0, 0);
      canvas.toBlob((blob) => {
        const pngUrl = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = pngUrl;
        link.download = `constellation-${constellation.name.toLowerCase().replace(/\s+/g, '-')}.png`;
        link.click();
        URL.revokeObjectURL(pngUrl);
        URL.revokeObjectURL(url);
      });
    };
    
    img.src = url;
  };

  return (
    <div className="constellation-card">
      <h3>{constellation.name}</h3>
      <svg 
        ref={svgRef}
        viewBox="0 0 100 100" 
        width="200" 
        height="200"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="100" height="100" fill="transparent" />
        {constellation.stars.map((star, i) => (
          <circle
            key={i}
            cx={star.x}
            cy={star.y}
            r={4}
            fill="#8b7fd8"
            opacity={1}
          />
        ))}
        {constellation.stars.map((star, i) => (
          i > 0 ? (
            <line
              key={`line-${i}`}
              x1={constellation.stars[i - 1].x}
              y1={constellation.stars[i - 1].y}
              x2={star.x}
              y2={star.y}
              stroke="#8b7fd8"
              strokeWidth="1.5"
              opacity={0.7}
            />
          ) : null
        ))}
      </svg>
      <div className="download-buttons">
        <button onClick={downloadSVG} className="download-btn">
          Download SVG
        </button>
        <button onClick={downloadPNG} className="download-btn">
          Download PNG
        </button>
      </div>
    </div>
  );
};

export default function ConstellationExporter() {
  return (
    <div className="constellation-exporter">
      <div className="exporter-header">
        <h1>Constellation Icon Exporter</h1>
        <p>Download any constellation design as an SVG or PNG file</p>
      </div>
      <div className="constellation-grid">
        {CONSTELLATIONS.map((constellation, idx) => (
          <ConstellationIcon key={idx} constellation={constellation} />
        ))}
      </div>
    </div>
  );
}

