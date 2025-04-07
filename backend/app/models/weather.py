import uuid
import json
from datetime import datetime
from app import db

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    rainfall = db.Column(db.Float, nullable=True)
    forecast = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, date, temperature=None, rainfall=None, forecast=None):
        self.id = uuid.uuid4()
        self.date = date
        self.temperature = temperature
        self.rainfall = rainfall
        self.forecast = forecast
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'date': self.date.isoformat(),
            'temperature': self.temperature,
            'rainfall': self.rainfall,
            'forecast': self.forecast,
            'created_at': self.created_at.isoformat()
        } 