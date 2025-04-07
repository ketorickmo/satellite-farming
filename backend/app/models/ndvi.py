import uuid
from datetime import datetime
from app import db

class NDVIHistory(db.Model):
    __tablename__ = 'ndvi_history'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    paddock_id = db.Column(db.UUID, db.ForeignKey('paddocks.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    ndvi_value = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    paddock = db.relationship('Paddock', back_populates='ndvi_history')
    
    def __init__(self, paddock_id, date, ndvi_value, image_url=None):
        self.id = uuid.uuid4()
        self.paddock_id = paddock_id
        self.date = date
        self.ndvi_value = ndvi_value
        self.image_url = image_url
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'paddock_id': str(self.paddock_id),
            'date': self.date.isoformat(),
            'ndvi_value': self.ndvi_value,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat()
        } 