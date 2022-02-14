from sqlite3 import Timestamp
from marshmallow import Schema, fields, post_load, validates, ValidationError
from db.db_manager import  Metric

class MetricSchema(Schema):
    sno = fields.Int()
    id = fields.Int()
    timestamp = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    temperature = fields.Float()
    humidity = fields.Float()

    @post_load
    def create_metric(self, data, **kwargs):
        return Metric(**data)

    @validates("humidity")
    def validate_humidity(self, value):
        if value < 0:
            raise ValidationError("humidity must be greater than 0.")
        if value > 100:
            raise ValidationError("humidity must not be greater than 100.")

    @validates("temperature")
    def validate_temperature(self, value):
        if value < -30:
            raise ValidationError("temperature must be greater than -30.")
        if value > 50:
            raise ValidationError("temperature must not be greater than 50.")

    @validates("id")
    def validate_id(self, value):
        if value >= 10000:
            raise ValidationError("id value should be less than 10000")

    @validates("id")
    def validate_timestamp(self, value):
        if value >= 10000:
            raise ValidationError("id value should be less than 10000")
