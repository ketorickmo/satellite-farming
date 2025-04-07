# Smart Farm Viewer Frontend

A Next.js application for viewing and managing farm paddocks with satellite imagery and NDVI data.

## Project Structure

```
src/
├── app/                    # Next.js app router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── globals.css        # Global styles
│   ├── components/        # React components
│   ├── utils/            # Utility functions
│   └── types/            # TypeScript type definitions
```

## Getting Started

1. Install dependencies:
```bash
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

## Features

- Interactive map for viewing and creating paddocks using Mapbox GL
- Satellite imagery integration
- Real-time updates

## Technologies

- Next.js 15
- TypeScript
- Mapbox GL JS
- React 19
- Tailwind CSS

## Development

The frontend is containerized using Docker and can be run as part of the full stack using:
```bash
docker compose -f compose.dev.yml up
```

This will start the frontend on http://localhost:3000 