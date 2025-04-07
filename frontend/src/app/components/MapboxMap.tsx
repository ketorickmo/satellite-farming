'use client';

import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import { MapboxMapProps } from '../types/mapbox';

import 'mapbox-gl/dist/mapbox-gl.css';

const MapboxMap: React.FC<MapboxMapProps> = ({
  initialCenter = [137.915, 36.259],
  initialZoom = 9,
  mapStyle = 'mapbox://styles/mapbox/satellite-v9',
  projection = 'globe',
  enableFog = true,
  className = ''
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const [mapInitialized, setMapInitialized] = useState(false);

  useEffect(() => {
    if (!mapContainerRef.current) {
      console.error("Map container ref is not available");
      return;
    }
    
    // Force the container to have dimensions before initializing Mapbox
    const container = mapContainerRef.current;
    container.style.width = '100%';
    container.style.height = '100%';
    
    // Get token from environment variable
    const token = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN;
    if (!token) {
      console.error('Mapbox token is missing');
      return;
    }
    
    // Set token
    mapboxgl.accessToken = token;
    
    // Initialize map
    try {
      const map = new mapboxgl.Map({
        container: container,
        style: mapStyle,
        projection: 'mercator',
        center: initialCenter,
        zoom: initialZoom,
        attributionControl: true,
        preserveDrawingBuffer: true
      });
      
      mapRef.current = map;

      // Add navigation controls
      map.addControl(new mapboxgl.NavigationControl(), 'top-right');
      
      // Wait for the map to load
      map.on('load', () => {
        console.log("Map loaded successfully");
        setMapInitialized(true);
      });

      // Debug any errors
      map.on('error', (e) => {
        console.error("Mapbox error:", e);
      });
    } catch (error) {
      console.error("Error initializing Mapbox:", error);
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
      }
    };
  }, [initialCenter, initialZoom, mapStyle, projection, enableFog]);

  return (
    <div 
      style={{ 
        width: '100%', 
        height: '100%', 
        position: 'relative' 
      }}
    >
      <div 
        ref={mapContainerRef} 
        className="map-container"
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: 0,
          right: 0,
        }}
      />
    </div>
  );
};

export default MapboxMap; 