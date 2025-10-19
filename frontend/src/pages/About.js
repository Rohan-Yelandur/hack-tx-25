import React from 'react';
import { FaLinkedin, FaVideo, FaFileAlt, FaLayerGroup, FaFlask, FaReact, FaCogs, FaGem, FaMicrophone } from 'react-icons/fa';
import './About.css';

export default function About() {
  return (
    <div className="about-page">
      <div className="about-hero">
        <h1 className="about-title">About Canopus</h1>
        <div className="mission">
          <p>
            Canopus is on a mission to democratize education by making high-quality,
            animated lessons accessible to everyone. We speed up lesson creation so
            educators can personalize learning at scale and learners can progress faster.
          </p>
        </div>
      </div>

      <div className="about-content">
        <section className="founders">
          <h2>Founders</h2>
          <ul>
            <li>
              <a href="https://www.linkedin.com/in/rohan-yelandur/" target="_blank" rel="noreferrer">
                Rohan Yelandur <FaLinkedin className="icon" />
              </a>
            </li>
            <li>
              <a href="https://www.linkedin.com/in/ayaansunesara/" target="_blank" rel="noreferrer">
                Ayaan Sunesara <FaLinkedin className="icon" />
              </a>
            </li>
            <li>
              <a href="https://www.linkedin.com/in/krishdhanuka4/" target="_blank" rel="noreferrer">
                Krish Dhanuka <FaLinkedin className="icon" />
              </a>
            </li>
            <li>
              <a href="https://www.linkedin.com/in/amogh-ajoy/" target="_blank" rel="noreferrer">
                Amogh Ajoy <FaLinkedin className="icon" />
              </a>
            </li>
          </ul>
        </section>

        <section className="tech">
          <h2>Technologies</h2>
          <ul className="tech-list">
            <li><FaVideo className="tech-icon"/> FFmpeg</li>
            <li><FaFileAlt className="tech-icon"/> LaTeX</li>
            <li><FaLayerGroup className="tech-icon"/> Manim</li>
            <li><FaFlask className="tech-icon"/> Flask</li>
            <li><FaCogs className="tech-icon"/> Multithreading</li>
            <li><FaGem className="tech-icon"/> Gemini</li>
            <li><FaMicrophone className="tech-icon"/> ElevenLabs</li>
            <li><FaReact className="tech-icon"/> React</li>
          </ul>
        </section>

      </div>
    </div>
  );
}
