import uuid
import json
from datetime import datetime
from app import db
from shapely.geometry import shape
from pyproj import Geod

class Paddock(db.Model):
    __tablename__ = 'paddocks'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    geometry = db.Column(db.Text, nullable=False)  # GeoJSON encoded as text
    area = db.Column(db.Float, nullable=False)  # Area in hectares
    agromonitoring_id = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ndvi_history = db.relationship('NDVIHistory', back_populates='paddock', cascade='all, delete-orphan')
    
    def __init__(self, name, geometry, agromonitoring_id=None):
        self.id = uuid.uuid4()
        self.name = name
        self.geometry = json.dumps(geometry) if isinstance(geometry, dict) else geometry
        self.area = self.calculate_area()
        self.agromonitoring_id = agromonitoring_id
    
    def calculate_area(self):
        """Calculate the area of the paddock in hectares"""
        geod = Geod(ellps="WGS84")
        geojson = json.loads(self.geometry) if isinstance(self.geometry, str) else self.geometry
        polygon = shape(geojson)
        
        # Calculate area in square meters and convert to hectares
        area_sqm = abs(geod.geometry_area_perimeter(polygon)[0])
        return area_sqm / 10000  # Convert square meters to hectares
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'geometry': json.loads(self.geometry) if isinstance(self.geometry, str) else self.geometry,
            'area': self.area,
            'agromonitoring_id': self.agromonitoring_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 