from flask_restful import Resource
from flask import jsonify, request
from marshmallow import Schema, fields, post_load, ValidationError
from db.db_manager import DataProcessor, Message, Sensor
from service.sensor_schema import SensorSchema

class SensorInspector(Resource):

    '''
        getting or deleting meta data specific to sensor id

        http://127.0.0.1:5000/sensors/id
            post - none
            get - retrive detail of sensor(id)
            delete: delete sensor(id)
            put: update the sensor data, if sensor id exist
    
    '''
    sensor_schema = SensorSchema()
  
    def __init__(self, session):
        self.session = session
        self.processor = DataProcessor()

    def get(self,id):
        result = self.processor.get_by_id(self.session, Sensor, id=id)
        return self.sensor_schema.dump(result)

    def put(self, id):
        
        self.processor.delete(self.session, Sensor, id=id)
        data = request.get_json(force=True)
        try:
            payload = self.sensor_schema.load(data)
        except ValidationError as err:
            msg = {Message.MSG_FAILED: err.messages}
            return msg, 400
        print(payload)
        self.processor.add(self.session, payload)


    def delete(self, id):
        count = self.processor.delete(self.session, Sensor, id=id)
        if count == 0:
            return {Message.MSG_FAILED: Message.MSG_NO_RECORD_FOUND}, 200
        else:
            return Message.MSG_SUCCESS, 200
            
    def post(self, id):
        return {Message.MSG_FAILED:Message.MSG_NOT_REQUIRED}, 200
       





