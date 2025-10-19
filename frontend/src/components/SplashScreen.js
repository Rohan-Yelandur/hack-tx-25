import { motion } from 'framer-motion';
import './SplashScreen.css';

function SplashScreen() {
  return (
    <motion.div
      className="splash-screen"
      initial={{ opacity: 1 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8, ease: 'easeInOut' }}
    >
      <motion.div
        className="splash-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      >
        <h1 className="splash-title">Canopus</h1>
        <p className="splash-subtitle">We Help You Connect the Dots</p>
      </motion.div>
    </motion.div>
  );
}

export default SplashScreen;

