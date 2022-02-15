from marshmallow import Schema, fields, post_load,validates, ValidationError
from db.db_manager import  Sensor

class SensorSchema(Schema):
    id = fields.Int()
    city = fields.Str()
    country = fields.Str()

    @post_load
    def create_sensor(self, data, **kwargs):
        return Sensor(**data)

    @validates("city")
    def validate_city(self, value):
        if len(value) >= 20:
            raise ValidationError("length of the city name should be lesser than 20")
      
    @validates("country")
    def validate_country(self, value):
        if len(value) >= 20:
            raise ValidationError("length of the country name should be lesser than 20")

    @validates("id")
    def validate_id(self, value):
        if value >= 10000:
            raise ValidationError("id value should be less than 10000")