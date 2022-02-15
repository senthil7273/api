from flask_restful import Resource
from flask import jsonify, request
from db.db_manager import Debugger, Message, Sensor, DataProcessor
from sqlalchemy.orm import Session
import marshmallow_dataclass
from marshmallow import Schema, fields, post_load, ValidationError
from service.sensor_schema import SensorSchema

class SensorManager(Resource):
    '''
        creating or deleting sensors

        http://127.0.0.1:5000/iot/api/v1.0/sensors - 
            post - registers new sensor(s)
            get - retrives all sensors
            delete: deletes all sensors
            put: (incomplete method)    
    '''
    sensor_schema = SensorSchema()
    sensors_schema = SensorSchema(many=True)

    def __init__(self, session):
        '''
            session: it holds the conversion with the db for any CRUD operations
            processor: performs basic CRUD operations  
        '''
        self.session = session
        self.processor = DataProcessor()

    def get(self):
        '''
            retrives all sensor(s) metadata from the db

            returns: jsonarray of sensor(s) metadata,
                     else {} is returned if no sensors found 
        
        '''
        result = self.processor.get_all(self.session, Sensor)
        return self.sensors_schema.dump(result)

    def put(self):
        '''
            incomplete method
        '''
        json_data = request.get_json(force=True)
        print(json_data)

    def delete(self):
        '''
            deletes all sensors from the table

            returns: success message on deleting all sensors,
                     warning message while sensors not found
        '''
        count = self.processor.delete_all(self.session, Sensor)
        if count == 0:
            return {Message.MSG_FAILED: Message.MSG_NO_RECORD_FOUND}, 200
        else:
            return Message.MSG_SUCCESS
           

    def post(self):
        '''
            registers new sensor(s) 

            input: array of sensor(s) or json object

            returns: success message on registering sensor successfully,
                     erro message on finding duplicate sensor or invalid sensor
        '''
        payload = None
        data = request.get_json(force=True)
        if isinstance(data, list):
            try:
                payload = self.sensor_schema.load(data, many=True)
            except ValidationError as err:
                msg = {Message.MSG_FAILED: err.messages}
                return msg, 400
        else:
            try:
                payload = self.sensor_schema.load(data)
            except ValidationError as err:
                msg = {Message.MSG_FAILED: err.messages}
                return msg, 400
        print(payload)
        try:
            self.processor.add(self.session, payload)
        except Exception as exp:
            return {Message.MSG_FAILED: exp.message}, 400
        return Message.MSG_SUCCESS, 200
        