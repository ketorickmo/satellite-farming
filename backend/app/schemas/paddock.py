from marshmallow import Schema, fields, validates, ValidationError
import json

class GeoJSONField(fields.Field):
    """Field that serializes to a GeoJSON dict and deserializes to a GeoJSON dict."""
    
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, str):
            return json.loads(value)
        return value
    
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        if isinstance(value, dict):
            # Validate GeoJSON structure
            if value.get('type') != 'Polygon':
                raise ValidationError('GeoJSON must be of type Polygon')
            if 'coordinates' not in value:
                raise ValidationError('GeoJSON must contain coordinates')
            return value
        elif isinstance(value, str):
            try:
                geojson = json.loads(value)
                if geojson.get('type') != 'Polygon':
                    raise ValidationError('GeoJSON must be of type Polygon')
                if 'coordinates' not in geojson:
                    raise ValidationError('GeoJSON must contain coordinates')
                return geojson
            except json.JSONDecodeError:
                raise ValidationError('Invalid GeoJSON format')
        raise ValidationError('Invalid GeoJSON format')

class PaddockSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    geometry = GeoJSONField(required=True)
    area = fields.Float(dump_only=True)
    agromonitoring_id = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('name')
    def validate_name(self, value):
        if len(value) < 1:
            raise ValidationError('Name must not be empty')
        if len(value) > 255:
            raise ValidationError('Name must be less than 255 characters')

paddock_schema = PaddockSchema()
paddocks_schema = PaddockSchema(many=True) 