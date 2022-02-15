from flask_restful import Resource
from flask import jsonify, request
import marshmallow_dataclass
from marshmallow import Schema, fields, post_load, ValidationError
from db.db_manager import Debugger, Message, Metric, DataProcessor
from service.metric_schema import MetricSchema

class SensorMetric(Resource):
    '''
        getting or deleting data specific to sensor id
            http://127.0.0.1:5000/sensors/id/metrics
                post - create new metric data
                get - get the average of metric data
                put - buk update of metrics data
                delete - delete the metrics data
    '''
    metric_schema = MetricSchema()
    metrics_schema = MetricSchema(many=True)
    

    def __init__(self, session):
        self.session = session
        self.processor = DataProcessor()

    def get(self, id):
        result = self.processor.get_by_id_all(self.session, Metric, id=id)
        if isinstance(result, list):
            return self.metrics_schema.dump(result)
        else:
            return self.metric_schema.dump(result)
      
    def put(self, id):
        return {Message.MSG_FAILED: Message.MSG_NOT_REQUIRED}, 200

    def delete(self, id):
        count = self.processor.delete(self.session, Metric, id=id)
        if count == 0:
            return {Message.MSG_FAILED: Message.MSG_NO_RECORD_FOUND}, 200
        else:
            return Message.MSG_SUCCESS, 200

    def post(self, id):
        data = request.get_json(force=True)
        if isinstance(data, list):
            try:
                payload = self.metrics_schema.load(data, many=True)
            except ValidationError as err:
                msg = {Message.MSG_FAILED: err.messages}
                return msg, 400
        else:
            try:
                payload = self.metric_schema.load(data)
            except ValidationError as err:
                msg = {Message.MSG_FAILED: err.messages}
                return msg, 400
        try:
            self.processor.add_by(self.session, payload)
        except Exception as exp:
            return {Message.MSG_FAILED: exp.message}, 400
        return Message.MSG_SUCCESS, 200