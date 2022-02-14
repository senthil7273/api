from urllib import response
from metrics_data import MetricData
import pytest
import requests

# eg http://127.0.0.1:5000/iot/api/v1.0/sensors/91/metrics

url_metric = 'http://127.0.0.1:5000/iot/api/v1.0/sensors/?/metrics'



def test_put_method():
    response = requests.put(url_metric.replace("?", "100"))
    data = response.json()
    assert data["failed"]
    assert data["failed"] == "method not required"


def test_post_method():
    url = url_metric.replace("?", "100")
    response = requests.post(url, data=MetricData.valid_metric)
    data = response.json()
    assert data["message"]

# def test_post_method():
#     response = requests.post(url_metric.replace("?", "100"), data=MetricData.valid_metrics)
#     data = response.json()
#     assert data["message"]
#     assert data["message"] == "succeed"

