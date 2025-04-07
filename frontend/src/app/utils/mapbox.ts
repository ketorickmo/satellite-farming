/**
 * Utility functions for Mapbox integration
 */

/**
 * Checks if the Mapbox token is available in the environment variables
 * @returns boolean indicating if token is available
 */
export const isMapboxTokenAvailable = (): boolean => {
  return !!process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN;
};

/**
 * Gets the Mapbox style URL for a specific style
 * @param style The style name (satellite, streets, outdoors, etc.)
 * @returns The full Mapbox style URL
 */
export const getMapboxStyle = (style: string): string => {
  const styles: Record<string, string> = {
    satellite: 'mapbox://styles/mapbox/satellite-v9',
    satelliteStreets: 'mapbox://styles/mapbox/satellite-streets-v12',
    outdoors: 'mapbox://styles/mapbox/outdoors-v12',
    light: 'mapbox://styles/mapbox/light-v11',
    dark: 'mapbox://styles/mapbox/dark-v11',
    streets: 'mapbox://styles/mapbox/streets-v12',
    navigationDay: 'mapbox://styles/mapbox/navigation-day-v1',
    navigationNight: 'mapbox://styles/mapbox/navigation-night-v1'
  };

  return styles[style] || styles.satellite;
};

/**
 * Common map center points for different regions
 */
export const MAP_CENTERS = {
  US: [-98.5795, 39.8283] as [number, number],
  Europe: [15.2551, 54.5260] as [number, number],
  Asia: [103.8198, 36.5617] as [number, number],
  Africa: [19.4902, 12.1090] as [number, number],
  SouthAmerica: [-58.9300, -13.1339] as [number, number],
  Australia: [134.0000, -25.0000] as [number, number],
  World: [0, 0] as [number, number]
}; 