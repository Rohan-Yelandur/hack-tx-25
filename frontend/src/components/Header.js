import './Header.css';
import { Link, useLocation } from 'react-router-dom';

function Header() {
  const location = useLocation();

  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="header-title">
          <h1>Manim Video Generator</h1>
        </Link>
        <nav className="header-nav">
          <Link
            to="/"
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link
            to="/community"
            className={`nav-link ${location.pathname === '/community' ? 'active' : ''}`}
          >
            Community
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
