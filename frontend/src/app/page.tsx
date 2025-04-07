import ClientMapWrapper from './components/ClientMapWrapper';

export default function Home() {
  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100vh', 
      width: '100vw',
      overflow: 'hidden'
    }}>
      <header style={{ 
        padding: '1rem', 
        backgroundColor: '#1f2937', 
        color: 'white' 
      }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Smart Farm Viewer</h1>
        <p style={{ fontSize: '0.875rem', opacity: 0.8 }}>Satellite imagery for agricultural analysis</p>
      </header>
      
      <main style={{ 
        flexGrow: 1, 
        position: 'relative',
        height: 'calc(100vh - 130px)'  /* Account for header & footer */
      }}>
        <ClientMapWrapper 
          initialCenter={[-98.5795, 39.8283]} // Center of the US
          initialZoom={4}
          mapStyle="mapbox://styles/mapbox/satellite-v9"
          enableFog={false}
          projection="mercator"
        />
      </main>
      
      <footer style={{ 
        padding: '0.5rem', 
        backgroundColor: '#f3f4f6', 
        color: '#4b5563', 
        fontSize: '0.875rem',
        textAlign: 'center'
      }}>
        Powered by Mapbox
      </footer>
    </div>
  );
}
