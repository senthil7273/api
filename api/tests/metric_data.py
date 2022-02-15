import datetime

class MetricData(object):

    def time(days=0):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
        return timestamp

    invalid_timestamp_metric = [{
        "id":"91",
        "temperature": 20,
        "humidity": 90,
        "timestamp": "{{CurrentDatetime}}"
    }]

    invalid_id_metric = [{
        "id":"9aa1",
        "temperature": 20,
        "humidity": 90,
        "timestamp": "{{CurrentDatetime}}"
    }]

    timestamp_missing_metric = [{
        "id":"100",
        "temperature": 20,
        "humidity": 90
    }]

    valid_metrics = [{
        "id":"1000",
        "temperature": 20,
        "humidity": 60,
        "timestamp": time()
        }, {
            "id":"1000",
            "temperature": 30,
            "humidity": 70,
            "timestamp": time()
        }, {
            "id":"1000",
            "temperature": 10,
            "humidity": 90,
            "timestamp": time()
    }]

    valid_metric = {
        "id":"1001",
        "temperature": 20,
        "humidity": 90,
        "timestamp": time()
    }

    unknown_sensor_metric ={
        "id":"5000",
        "temperature": 20,
        "humidity": 90,
        "timestamp": time()
    }
