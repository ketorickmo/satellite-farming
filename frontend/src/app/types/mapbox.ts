// Mapbox projection options
export type MapboxProjection = 'globe' | 'mercator' | 'albers' | 'equalEarth' | 'equirectangular' | 'lambertConformalConic' | 'naturalEarth' | 'winkelTripel';

// Props for the Mapbox map component
export interface MapboxMapProps {
  initialCenter?: [number, number];
  initialZoom?: number;
  mapStyle?: string;
  projection?: MapboxProjection;
  enableFog?: boolean;
  className?: string;
} 