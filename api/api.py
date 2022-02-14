from flask import Flask
from flask_restful import Api
from service.metrics_api import MetricManager
from service.sensor_api import SensorInspector
from service.sensor_manager_api import SensorManager
from service.sensor_metric_api import SensorMetric
from db.db_manager import DBManager, Debugger

class App:

    app = Flask(__name__)
    api = Api(app)
    session = None
    
    def init_app(self):        
        db = DBManager()
        session = db.session
        engine = db.engine
        Debugger.table_exists(engine,"sensors")
        self.api.add_resource(SensorManager, '/iot/api/v1.0/sensors', resource_class_kwargs={'session': session})
        self.api.add_resource(SensorInspector, '/iot/api/v1.0/sensors/<int:id>',  resource_class_kwargs={'session': session})
        self.api.add_resource(SensorMetric, '/iot/api/v1.0/sensors/<int:id>/metrics', resource_class_kwargs={'session': session})
        self.api.add_resource(MetricManager, '/iot/api/v1.0/metrics', resource_class_kwargs={'session': session})
        self.app.run(debug=True)

if __name__ == "__main__":
    app = App()
    app.init_app()