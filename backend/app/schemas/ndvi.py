from marshmallow import Schema, fields, validates, ValidationError

class NDVISchema(Schema):
    id = fields.UUID(dump_only=True)
    paddock_id = fields.UUID(required=True)
    date = fields.DateTime(required=True)
    ndvi_value = fields.Float(required=True)
    image_url = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    
    @validates('ndvi_value')
    def validate_ndvi_value(self, value):
        # NDVI values typically range from -1 to 1
        if value < -1 or value > 1:
            raise ValidationError('NDVI value must be between -1 and 1')

ndvi_schema = NDVISchema()
ndvi_list_schema = NDVISchema(many=True) 