from flask_restful import Resource
from flask import jsonify, request
from marshmallow import Schema, fields, post_load, ValidationError
from db.db_manager import DataProcessor, Message, Sensor
from service.sensor_schema import SensorSchema

class SensorInspector(Resource):

    '''
        getting or deleting sensor & its metadata based on its id.

        http://127.0.0.1:5000/iot/api/v1.0/sensors/820
            post - Method not needed.
            get - retrives the metadata of a sensor(id)
            delete: deletes a sensor(id)
            put: (Incomplete method) update the sensor data, if the sensor id exist
    
    '''
    sensor_schema = SensorSchema()
  
    def __init__(self, session):
        '''
            session: it holds the conversion with the db for any CRUD operations
            processor: performs basic CRUD operations  
        '''
        self.session = session
        self.processor = DataProcessor()

    def get(self,id):
        '''
            retrives the metadata of a sensor(id)

            id: sensor's id

            returns: returns the json object, if found,
                     else empty object: {} is returned
        '''
        result = self.processor.get_by_id(self.session, Sensor, id=id)
        return self.sensor_schema.dump(result)

    def put(self, id):
        '''
            Its an incomplete method
        '''
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
        '''
            deletes a sensor from the db based on its id.

            id: sensor's id

            returns: it returns "success" message on deleting the sensor.
                     else, failed message is returned.
        '''
        count = self.processor.delete(self.session, Sensor, id=id)
        if count == 0:
            return {Message.MSG_FAILED: Message.MSG_NO_RECORD_FOUND}, 200
        else:
            return Message.MSG_SUCCESS, 200
            
    def post(self, id):
        '''
            post method is not needed as SensorManager api is available for adding sensor(s)
        '''
        return {Message.MSG_FAILED:Message.MSG_NOT_REQUIRED}, 200
       





