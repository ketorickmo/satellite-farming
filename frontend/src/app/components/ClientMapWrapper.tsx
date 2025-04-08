'use client'

import dynamic from 'next/dynamic';
import { MapboxMapProps } from '../types/mapbox';
import MapControls from './MapControls';
import { useRef } from 'react';
import type { MapboxMapRef } from './MapboxMap';

// Dynamic import with ssr: false is valid in a Client Component
const MapboxMap = dynamic(
  () => import('./MapboxMap'),
  { 
    ssr: false,
    loading: () => (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f0f0f0'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div>Loading map...</div>
        </div>
      </div>
    )
  }
);

export default function ClientMapWrapper(props: MapboxMapProps) {
  const mapRef = useRef<MapboxMapRef>(null);

  const handleZoomIn = () => {
    if (mapRef.current) {
      mapRef.current.zoomIn();
    }
  };

  const handleZoomOut = () => {
    if (mapRef.current) {
      mapRef.current.zoomOut();
    }
  };

  const handleReset = () => {
    if (mapRef.current && props.initialCenter && props.initialZoom) {
      mapRef.current.flyTo({
        center: props.initialCenter,
        zoom: props.initialZoom,
        duration: 1000
      });
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <MapboxMap {...props} ref={mapRef} />
      <MapControls 
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onReset={handleReset}
      />
    </div>
  );
} 