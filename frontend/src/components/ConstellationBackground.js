import { useEffect, useRef } from 'react';
import './ConstellationBackground.css';

function ConstellationBackground() {
  const canvasRef = useRef(null);
  const mouseRef = useRef({ x: -1000, y: -1000 });
  const starsRef = useRef([]);
  const constellationsRef = useRef([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationFrameId;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize stars with spacing
    const initStars = () => {
      starsRef.current = [];
      const numStars = 35; // Reduced for more spacing
      const minDistance = 80; // Minimum distance between stars
      
      for (let i = 0; i < numStars; i++) {
        let attempts = 0;
        let newStar;
        
        // Try to place star with minimum spacing
        do {
          newStar = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 1 + 0.5, // Smaller: 0.5 to 1.5 (was 1 to 3)
            brightness: Math.random() * 0.5 + 0.5,
            twinkleSpeed: Math.random() * 0.02 + 0.01
          };
          attempts++;
        } while (
          attempts < 50 && 
          starsRef.current.some(star => 
            Math.hypot(star.x - newStar.x, star.y - newStar.y) < minDistance
          )
        );
        
        starsRef.current.push(newStar);
      }
    };

    // Create constellation groups (8-10 groups with 3-5 stars each)
    const initConstellations = () => {
      constellationsRef.current = [];
      const numConstellations = Math.floor(Math.random() * 3) + 8; // 8-10 constellations
      const stars = starsRef.current;
      const usedStars = new Set();

      for (let i = 0; i < numConstellations; i++) {
        const constellation = [];
        const numStarsInConstellation = Math.floor(Math.random() * 3) + 3; // 3-5 stars
        
        // Pick a random starting star
        let startIndex;
        do {
          startIndex = Math.floor(Math.random() * stars.length);
        } while (usedStars.has(startIndex));
        
        constellation.push(startIndex);
        usedStars.add(startIndex);

        // Add nearby stars to form constellation
        for (let j = 1; j < numStarsInConstellation; j++) {
          const lastStar = stars[constellation[constellation.length - 1]];
          let closestIndex = -1;
          let closestDist = Infinity;

          // Find closest unused star within closer distance (max 150px, was 200px)
          for (let k = 0; k < stars.length; k++) {
            if (usedStars.has(k)) continue;
            
            const dist = Math.hypot(stars[k].x - lastStar.x, stars[k].y - lastStar.y);
            if (dist < closestDist && dist < 150) {
              closestDist = dist;
              closestIndex = k;
            }
          }

          if (closestIndex !== -1) {
            constellation.push(closestIndex);
            usedStars.add(closestIndex);
          } else {
            break; // No more nearby stars
          }
        }

        if (constellation.length >= 2) {
          constellationsRef.current.push(constellation);
        }
      }
    };

    initStars();
    initConstellations();

    // Mouse move handler
    const handleMouseMove = (e) => {
      mouseRef.current = { x: e.clientX, y: e.clientY };
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const mouse = mouseRef.current;
      const mouseRadius = 200; // Trigger radius

      // Draw constellation lines first (behind stars)
      constellationsRef.current.forEach(constellation => {
        for (let i = 0; i < constellation.length - 1; i++) {
          const star1 = starsRef.current[constellation[i]];
          const star2 = starsRef.current[constellation[i + 1]];

          // Calculate distances from mouse to each star
          const dist1 = Math.hypot(star1.x - mouse.x, star1.y - mouse.y);
          const dist2 = Math.hypot(star2.x - mouse.x, star2.y - mouse.y);
          const minDist = Math.min(dist1, dist2);

          // Calculate opacity based on proximity
          let opacity = 0.1; // Base dim opacity
          if (minDist < mouseRadius) {
            const proximity = 1 - (minDist / mouseRadius);
            opacity = 0.1 + (proximity * 0.5); // Fade from 0.1 to 0.6
          }

          // Draw line
          ctx.beginPath();
          ctx.moveTo(star1.x, star1.y);
          ctx.lineTo(star2.x, star2.y);
          ctx.strokeStyle = `rgba(0, 255, 255, ${opacity})`; // Cyan color
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      });

      // Draw stars
      starsRef.current.forEach((star, index) => {
        // Update twinkle
        star.brightness += star.twinkleSpeed;
        if (star.brightness > 1 || star.brightness < 0.5) {
          star.twinkleSpeed *= -1;
        }

        // Calculate distance from mouse
        const dist = Math.hypot(star.x - mouse.x, star.y - mouse.y);
        
        // Calculate glow intensity based on proximity
        let glowIntensity = star.brightness * 0.5; // Base brightness
        let starSize = star.size; // Keep size constant, no growth
        
        if (dist < mouseRadius) {
          const proximity = 1 - (dist / mouseRadius);
          glowIntensity = star.brightness * (0.5 + proximity * 0.5); // 0.5 to 1.0
          // Removed size growth to keep stars small
        }

        // Draw star glow (smaller glow radius: 2x instead of 3x)
        const gradient = ctx.createRadialGradient(star.x, star.y, 0, star.x, star.y, starSize * 2);
        gradient.addColorStop(0, `rgba(255, 255, 255, ${glowIntensity})`);
        gradient.addColorStop(0.3, `rgba(0, 255, 255, ${glowIntensity * 0.5})`);
        gradient.addColorStop(1, 'rgba(0, 255, 255, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(star.x, star.y, starSize * 2, 0, Math.PI * 2);
        ctx.fill();

        // Draw star core
        ctx.fillStyle = `rgba(255, 255, 255, ${glowIntensity})`;
        ctx.beginPath();
        ctx.arc(star.x, star.y, starSize, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return <canvas ref={canvasRef} className="constellation-background" />;
}

export default ConstellationBackground;
