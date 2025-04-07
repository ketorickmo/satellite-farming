# Smart Farm Viewer

A full-stack application for viewing and managing farm paddocks with satellite imagery and NDVI data.

## Project Structure

```
.
├── frontend/               # Next.js frontend application
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   │   ├── layout.tsx # Root layout
│   │   │   ├── page.tsx   # Home page
│   │   │   ├── components/# React components
│   │   │   ├── utils/     # Utility functions
│   │   │   └── types/     # TypeScript type definitions
│   │   └── ...
│   └── ...
│
└── backend/               # Flask backend application
    ├── app/
    │   ├── api/          # API endpoints
    │   ├── models/       # Database models
    │   ├── schemas/      # Data validation schemas
    │   ├── services/     # Business logic
    │   └── utils/        # Utility functions
    └── ...
```

## Getting Started

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
Create a `.env.development` file with:
```
NEXT_PUBLIC_API_URL=http://localhost:5001
```

3. Run the development server:
```bash
npm run dev
```

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env.development` file with:
```
FLASK_APP=run.py
FLASK_DEBUG=1
DATABASE_URL=postgresql://smartfarm:dev_password@localhost:5432/smartfarm
```

3. Run the development server:
```bash
python run.py
```

## Features

- Interactive map for viewing and creating paddocks using Mapbox GL
- Satellite imagery integration
- Real-time updates
- RESTful API for farm data management
- PostgreSQL database with PostGIS for spatial data

## Technologies

### Frontend
- Next.js 15
- TypeScript
- Mapbox GL JS
- React 19
- Tailwind CSS

### Backend
- Flask
- SQLAlchemy
- PostgreSQL with PostGIS
- Flask-RESTful
- Marshmallow

## Development

The application is containerized using Docker and can be run as a full stack using:
```bash
docker compose -f compose.dev.yml up
```

This will start:
- Frontend on http://localhost:3000
- Backend on http://localhost:5001
- PostgreSQL on localhost:5432
