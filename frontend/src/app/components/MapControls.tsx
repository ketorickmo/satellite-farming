'use client'

import { Button } from "@/components/ui/button"
import { MapboxMapProps } from "../types/mapbox"

interface MapControlsProps {
  onZoomIn: () => void
  onZoomOut: () => void
  onReset: () => void
}

export default function MapControls({ onZoomIn, onZoomOut, onReset }: MapControlsProps) {
  return (
    <div className="absolute top-4 right-4 flex flex-col gap-2 bg-white/90 p-2 rounded-xl shadow-lg backdrop-blur-sm border border-gray-200">
      <Button 
        variant="outline" 
        size="icon"
        onClick={onZoomIn}
        className="h-9 w-9 hover:bg-blue-50 hover:text-blue-600 transition-colors"
        title="Zoom in"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </Button>
      <Button 
        variant="outline" 
        size="icon"
        onClick={onZoomOut}
        className="h-9 w-9 hover:bg-blue-50 hover:text-blue-600 transition-colors"
        title="Zoom out"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </Button>
      <Button 
        variant="outline" 
        size="icon"
        onClick={onReset}
        className="h-9 w-9 hover:bg-blue-50 hover:text-blue-600 transition-colors"
        title="Reset view"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
          <path d="M3 3v5h5"></path>
        </svg>
      </Button>
    </div>
  )
} 