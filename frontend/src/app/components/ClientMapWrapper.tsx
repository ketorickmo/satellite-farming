'use client'

import dynamic from 'next/dynamic';
import { MapboxMapProps } from '../types/mapbox';

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
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <MapboxMap {...props} />
    </div>
  );
} 