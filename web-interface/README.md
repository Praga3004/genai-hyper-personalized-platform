# Frontend - Tamil Nadu Election Campaign Platform

React web application for managing voters and generating hyper-personalized campaign messages.

## Prerequisites

- Node.js 14+ and npm
- Backend API running (see `../python-backend/README.md`)

## Installation

1. **Install dependencies:**
   ```bash
   cd web-interface
   npm install
   ```

2. **Configure API URL:**
   Create a `.env` file in the `web-interface` directory:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```
   For production, set this to your deployed backend URL.

## Running the Application

### Development Mode

```bash
npm start
```

Runs the app in development mode at [http://localhost:3000](http://localhost:3000).

### Production Build

```bash
npm run build
```

Builds the app for production to the `build` folder.

## Features

- **Voter Management**: Browse and filter voters from Supabase database
- **Advanced Filtering**: Filter by category, issue, gender, location, age, and search by name/ID
- **Bulk Selection**: Select multiple voters using checkboxes
- **Campaign Generation**: Generate personalized Tamil and English campaign messages for selected voters
- **Results View**: View generated messages in a scrollable table with click-to-view details

## Project Structure

```
src/
├── components/
│   ├── FilterBar.js          # Filter controls
│   ├── PeopleTable.js        # Voter table with selection
│   ├── GenerateContentBar.js # Generate button
│   └── ResultTable.js        # Results display
├── App.js                    # Main application component
└── App.css                   # Global styles
```

## API Integration

The frontend connects to the backend API at the URL specified in `REACT_APP_API_BASE_URL`:

- `GET /api/voters` - Fetch voters with filters
- `GET /api/voters/filters/options` - Get filter dropdown options
- `POST /api/generate-campaign-from-ids` - Generate campaign messages

## Deployment

The app can be deployed to any static hosting service (Vercel, Netlify, etc.):

1. Build the app: `npm run build`
2. Deploy the `build` folder
3. Set `REACT_APP_API_BASE_URL` environment variable to your backend URL
