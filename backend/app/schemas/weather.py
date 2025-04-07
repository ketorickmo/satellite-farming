from marshmallow import Schema, fields

class WeatherSchema(Schema):
    id = fields.UUID(dump_only=True)
    date = fields.DateTime(required=True)
    temperature = fields.Float(allow_none=True)
    rainfall = fields.Float(allow_none=True)
    forecast = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

weather_schema = WeatherSchema()
weather_list_schema = WeatherSchema(many=True) 