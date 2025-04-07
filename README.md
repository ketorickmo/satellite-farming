# Smart Farm Viewer Frontend

A Next.js application for viewing and managing farm paddocks with satellite imagery and NDVI data.

## Project Structure

```
src/
├── app/                    # Next.js app router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── paddocks/          # Paddock-related pages
│       ├── page.tsx       # Paddocks list
│       ├── new/           # New paddock creation
│       └── [id]/          # Individual paddock view
├── components/            # React components
│   ├── map/              # Map-related components
│   ├── paddocks/         # Paddock-related components
│   ├── weather/          # Weather-related components
│   └── ui/               # Reusable UI components
└── lib/                  # Shared utilities
    ├── api/              # API client
    ├── hooks/            # Custom React hooks
    ├── store/            # State management
    ├── types/            # TypeScript types
    └── utils/            # Utility functions
```

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
Create a `.env.local` file with:
```
NEXT_PUBLIC_API_URL=http://localhost:5001
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
```

3. Run the development server:
```bash
npm run dev
```

## Features

- Interactive map for viewing and creating paddocks
- NDVI data visualization
- Weather information
- Satellite imagery integration
- Real-time updates

## Technologies

- Next.js 14
- TypeScript
- Mapbox GL JS
- TanStack Query
- Zustand
- Tailwind CSS
- Recharts 