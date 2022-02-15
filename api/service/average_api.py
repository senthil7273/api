from flask_restful import Resource
from flask import jsonify, request
import marshmallow_dataclass
from marshmallow import Schema, fields, post_load, ValidationError
from db.db_manager import Debugger, Message, Metric, DataProcessor
from service.metric_schema import MetricSchema

class AverageMetric(Resource):
    '''
        getting or deleting data specific to sensor id
            http://127.0.0.1:5000/iot/api/v1.0/sensors/83/average
                post - create new metric data
                get - get the average of metric data
                put - buk update of metrics data
                delete - delete the metrics data
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
            Returns the average of temperature & humidity specific to a sensor.

            returns:
                returns the average, if the id:30 is found.

                {"avg_temperature":40,
                "avg_humidity": 20,
                "id":30}

                returns the average(0), if the id:31 is  not found.
                
                {"avg_temperature":0,
                "avg_humidity": 0,
                "id":31}

        '''
        result = self.processor.get_avg_by_id(self.session, Metric, id=id)
        print(result)
        return result
      
    def put(self, id):
        '''
            This method is not needed as of now
        '''
        return {Message.MSG_FAILED: Message.MSG_NOT_REQUIRED}, 200

    def delete(self, id):
        '''
            This method is not needed as of now
        '''
        return {Message.MSG_FAILED: Message.MSG_NOT_REQUIRED}, 200

    def post(self, id):
        '''
            This method is not needed as of now
        '''
        return {Message.MSG_FAILED: Message.MSG_NOT_REQUIRED}, 200