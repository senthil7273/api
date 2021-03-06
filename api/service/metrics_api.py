from xmlrpc.client import Boolean
from flask_restful import Resource, abort
from flask import jsonify, request
import marshmallow_dataclass
from marshmallow import Schema, fields, post_load
from marshmallow import validates, ValidationError, validates_schema
from db.db_manager import Debugger, Message, Metric, DataProcessor
from service.metric_schema import MetricSchema
from sqlalchemy import Table, Column, String, MetaData, ForeignKey
from sqlalchemy import Float, Integer, DATETIME, delete, update
from sqlalchemy.orm import declarative_base
import datetime

class ReportSchema(Schema):
    average = fields.Boolean(required=True, \
        error_messages={"required": {"message": "average value required", "code": 400}})

    start_date = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    end_date =  fields.DateTime(format='%Y-%m-%dT%H:%M:%S')

    @validates("start_date")
    def validate_start_date(self, value):
        if value >= datetime.datetime.now():
            raise ValidationError("start_date must be lesser than end_date or current time.")
      
    @validates_schema
    def validate_date(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] >= data['end_date']:
                    raise ValidationError("start_date must be lesser than end_date.")
    
    @validates("end_date")
    def validate_end_date(self, value):
        if value >= datetime.datetime.now():
            raise ValidationError("end_date must be less than or equal to current time")


class MetricManager(Resource):
    '''
        getting or deleting sensor's metrics data

        http://127.0.0.1:5000/iot/api/v1.0/metrics
            post - posts metric(s) to the db
            get - retrives the metrics(average of all, from & to date) of sensors
            delete: deletes all metrics data
            put: This method is not needed
    
    '''
    
    metrics_schema = MetricSchema(many=True)
    metric_schema = MetricSchema()
    report_schema = ReportSchema()

    def __init__(self, session):
        '''
            session: it holds the conversion with the db for any CRUD operations
            processor: performs basic CRUD operations  
        '''
        self.session = session
        self.processor = DataProcessor()

    def get(self):
        '''
            retrives the metrics(average of all, from & to date) of sensors
            {
                "average": false,
                "start_date": "{{fromTime}}"
                "end_date": "{{endTime}}"
            }

            average: true - it returns the average(all sensors) of temperature & the humidity
            average: false - it returns the metrics record(s) based on the timestamp(start_date, end_date)

        '''
        data = request.get_json(force=True)
        try:
            payload = self.report_schema.load(data)
        except ValidationError as err:
            msg = {Message.MSG_FAILED: err.messages}
            return msg, 400
        
        if payload['average'] == True:
            average = self.processor.get_average(self.session, Metric)
            return average
        else:
            records = self.processor.get_metrics_by_date(self.session, Metric, payload)
            return self.metrics_schema.dump(records)
           
    def delete(self):
        '''
            deletes all metrics, literally clears the table
        '''
        count = self.processor.delete_all(self.session, Metric)
        if count <= 0:
            return {Message.MSG_FAILED: Message.MSG_NO_RECORD_FOUND}, 200
        else:
            return Message.MSG_SUCCESS, 200

    def put(self):
        '''
            this method is not needed
        '''
        return {Message.MSG_FAILED:Message.MSG_NOT_REQUIRED}, 200

    def post(self):
        '''
            adds metric(s) to the db based on the sensor's id.

            if unknown sensor is detected or unknown parameter is in the metric data, 
            transaction will be declined with the error message.

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
        print(payload)
        try:
            self.processor.add_by(self.session, payload)
        except Exception as exp:
            print(exp.message)
            return {Message.MSG_FAILED: exp.message}, 400
        return Message.MSG_SUCCESS, 200


