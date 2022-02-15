# POC: Simple Rest APIs 


### Needed extension/libs/tools
    Extensions/libs/tools stack used for this POC are
        * flask
        * flask restful
        * sqlalchemy
        * marshmallow
        * pytest

### Versions
#### versions of frameworks/tools used to develop this POC
```bash
#!/bin/bash
flask '1.1.2'
sqlalchemy '1.4.31'
marshmallow '3.14.1'
pytest '6.1.1'
```


### Installation
#### Install the following extension/libs/tools to run this POC
```bash
#!/bin/bash
pip install flask
pip install flask-restful
pip install sqlalchemy
pip install marshmallow-dataclass
pip install -U pytest
```

### Exposed Api(s)
Here is the list of exposed APIs & its methods

* Register, Delete, Retrive Sensors
(http://127.0.0.1:5000/iot/api/v1.0/sensors)
* Delete, Retrive Sensor
(http://127.0.0.1:5000/iot/api/v1.0/sensors/820)
* Retrive, Delete, Post metric(s) of a Sensor
(http://127.0.0.1:5000/iot/api/v1.0/sensors/100/metrics)
* Retrive, Delete, Post metric(s) of Sensors
(http://127.0.0.1:5000/iot/api/v1.0/metrics)
* Retrive the average metric of a  Sensor
(http://127.0.0.1:5000/iot/api/v1.0/sensors/83/average)

### Service Flask APIs
Run the python script api.py to initiate the flask rest api(s).

```bash
api\api>python api.py
```
output:

```bash
Table "sensors" exists: True
 * Serving Flask app "api" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with windowsapi reloader
```

### Unit Tests
Here is the instructions to run unit tests.

Make sure, the service is up & running before initiating unit tests.
Then, run the following command to initate unit tests.

```bash
\api\api\tests>pytest test_senson_manager_api.py test_metric_api.py test_sensor_api.py test_metrics_api.py
```

output:
```bash
collected 27 items

test_senson_manager_api.py ........                                                                                                                             [ 29%]
test_metric_api.py .......                                                                                                                                      [ 55%]
test_sensor_api.py .....                                                                                                                                        [ 74%]
test_metrics_api.py .......                                                                                                                                     [100%]

========================================================================== warnings summary ==========================================================================
..\..\..\..\..\Anaconda3\lib\site-packages\pyreadline\py3k_compat.py:8
  C:\Users\91995\Anaconda3\lib\site-packages\pyreadline\py3k_compat.py:8: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3, and in 3.9 it will stop working
    return isinstance(x, collections.Callable)

-- Docs: https://docs.pytest.org/en/stable/warnings.html
=================================================================== 27 passed, 1 warning in 0.69s ====================================================================
```

Unit tests should be run in the given order(test scripts) above as the setup & tear down is not yet implemented.

* To re-run all unit tests, 
    * stop the flask api service
    * clear the test.db file created in the local directory (/api/api/local.db)
    * service the api
    * run the test cases