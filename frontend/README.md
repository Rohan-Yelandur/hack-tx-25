# Manim Video Generator - Frontend

React frontend for the AI-powered Manim video generator.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.js
│   └── Header.css
├── pages/              # Page components
│   ├── VideoGenerator.js
│   └── VideoGenerator.css
├── config/             # Configuration files
│   └── constants.js    # API URLs and constants
├── App.js              # Main app component
├── App.css             # Global styles
└── index.js            # Entry point
```

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm start
```

Runs the app at [http://localhost:3000](http://localhost:3000)

### Build

```bash
npm run build
```

Builds the app for production to the `build` folder.

## Configuration

Update API base URL in `src/config/constants.js`:

```javascript
export const API_BASE_URL = 'http://localhost:5000';
```

## Features

- ✨ Clean, modular component structure
- 🎨 Responsive design with gradient UI
- 🎬 Real-time video generation and playback
- 📝 Collapsible code viewer
- ⚡ Loading states and error handling


### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
