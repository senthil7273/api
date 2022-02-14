from urllib import response
from metric_data import MetricData
import pytest
import requests

# eg http://127.0.0.1:5000/iot/api/v1.0/sensors/91/metrics

url_metric = 'http://127.0.0.1:5000/iot/api/v1.0/sensors/?/metrics'



def test_put_method():
    '''
        put method is not needed as sensor streams data
    '''
    response = requests.put(url_metric.replace("?", "100"))
    data = response.json()
    assert data["failed"]
    assert data["failed"] == "method not required"


def test_post_metric():
    '''
       Inserting a metric for the sensor 1001
    '''
    url = url_metric.replace("?", "1001")
    response = requests.post(url, json=MetricData.valid_metric)
    data = response.json()
    print(f'data  {data}')
    assert data["message"]
    assert data["message"] == "succeed"

def test_post_metrics():
    '''
        Inserting metrics for the sensor 1000
    '''
    url = url_metric.replace("?", "1000")
    response = requests.post(url, json=MetricData.valid_metrics)
    data = response.json()
    assert data["message"]
    assert data["message"] == "succeed"

def test_get_metric():
    '''
        number of metrics for the sensor:1000 should be > 1
    '''
    response = requests.get(url_metric.replace("?", "1000"))
    data = response.json()
    assert data is not None
    assert len(data) > 1


def test_get_metric():
    '''
        number of metrics for the sensor:1001 should be 1
    '''
    response = requests.get(url_metric.replace("?", "1001"))
    data = response.json()
    assert data is not None
    assert len(data) == 1


def test_get_metric():
    '''
        number of metrics for the sensor:1003 should be 0 as no metrics found.
    '''
    response = requests.get(url_metric.replace("?", "1003"))
    data = response.json()
    assert data is not None
    assert len(data) == 0

def test_delete_unknown_metric():
    '''
        delete metrics of unknown sensor.
    '''
    response = requests.delete(url_metric.replace("?", "1003"))
    data = response.json()
    assert data["failed"]
    assert data["failed"] == "no record found"

def test_delete_known_metric():
    '''
        delete metrics of known sensor.
    '''
    response = requests.delete(url_metric.replace("?", "1001"))
    data = response.json()
    assert data["message"]
    assert data["message"] == "succeed"


def test_post_invalid_sensor_metric():
    '''
        Inserting metrics for the sensor 1000
    '''
    url = url_metric.replace("?", "5000")
    response = requests.post(url, json=MetricData.unknown_sensor_metric)
    data = response.json()
    assert data["failed"]
    assert data["failed"] == "Unknown sensor found"