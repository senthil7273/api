from flask_restful import Resource
from flask import jsonify, request
import marshmallow_dataclass
from marshmallow import Schema, fields, post_load, ValidationError
from db.db_manager import Debugger, Message, Metric, DataProcessor
from service.metric_schema import MetricSchema

class SensorMetric(Resource):
    '''
        getting or deleting metric data specific to a sensor id
            http://127.0.0.1:5000/iot/api/v1.0/sensors/100/metrics
                post - posts new metric data of a sensor
                get - retrives the metrics of a sensor(id)
                put - method not needed
                delete - deletes the metric of a sensor
    '''
    metric_schema = MetricSchema()
    metrics_schema = MetricSchema(many=True)
    

    def __init__(self, session):
        '''
            session: it holds the conversion with the db for any CRUD operations
            processor: performs basic CRUD operations  
        '''
        self.session = session
        self.processor = DataProcessor()

    def get(self, id):
        '''
            retrives the metrics of a sensor(id)

            id: sensor's id

            returns: returns the json object, if found,
                     else empty object: {} is returned
        '''
        result = self.processor.get_by_id_all(self.session, Metric, id=id)
        if isinstance(result, list):
            return self.metrics_schema.dump(result)
        else:
            return self.metric_schema.dump(result)
      
    def put(self, id):
        '''
           This method is not neeed as we post the metrics
        '''
        return {Message.MSG_FAILED: Message.MSG_NOT_REQUIRED}, 200

    def delete(self, id):
        '''
            deletes all metrics specific to a sensor(id)

            id: sensor's id

            returns: returns success message on deleting metrics data.
                     else Warning message is returned, if no record or sensor found
        '''
        count = self.processor.delete(self.session, Metric, id=id)
        if count == 0:
            return {Message.MSG_FAILED: Message.MSG_NO_RECORD_FOUND}, 200
        else:
            return Message.MSG_SUCCESS, 200

    def post(self, id):
        '''
            posts the metric(s) specific to a sensor(id)

            id: sensor's id

            returns: returns success messageon adding the metrics,
                     else warning message is returend if unknown sensor is detected.
        '''
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