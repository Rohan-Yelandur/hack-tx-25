import './Header.css';
import { Link, useLocation } from 'react-router-dom';

function Header() {
  const location = useLocation();

  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="header-title">
          <img src="/constellation-scorpius.svg" alt="Canopus Logo" className="header-logo" />
          <h1>Canopus</h1>
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
          <Link
            to="/about"
            className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}
          >
            About
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
