from urllib import response
from metrics_data import MetricsData
import pytest
import requests



# The root url of the flask api
url_metrics = 'http://127.0.0.1:5000/iot/api/v1.0/metrics' 


def test_invalid_timestamp_metrics():
  '''
  posting an invalid metric data with an invalid timestamp should be failed
  {
    "failed": {
        "0": {
            "timestamp": [
                "Not a valid datetime."
            ]
        }
    }
}
  '''

  response = requests.post(url_metrics, json=MetricsData.invalid_timestamp_metric)
  data = response.json()
  assert data["failed"]
  assert data["failed"]["0"]
  assert data["failed"]["0"]["timestamp"]

def test_invalid_id_metrics():
  '''
  posting a metric with an invalid sensor id should be failed
    {
      "failed": {
          "0": {
              "id": [
                  "Not a valid integer."
              ]
          }
      }
    }
  '''

  response = requests.post(url_metrics, json=MetricsData.invalid_id_metric)
  data = response.json()
  assert data["failed"]
  assert data["failed"]["0"]
  assert data["failed"]["0"]["id"]


# def test_missing_timestamp():
#   '''
#   posting a metric data with an missing timestamp should be failed
#   '''
#   response = requests.post(url_metrics, json=MetricsData.timestamp_missing_metric)
#   data = response.json()
#   assert data["failed"]
#   assert data["failed"] == "duplicate sensor or missing k/v pairs"


def test_post_valid_metrics():
  '''
  valid metrics data should be ingested
  '''
  response = requests.post(url_metrics, json=MetricsData.valid_metrics)
  data = response.json()
  assert data["message"]
  assert data["message"] == "succeed"

def test_delete_all_metrics():
  '''
   Should able to delete all metrics data
  '''
  response = requests.delete(url_metrics)
  data = response.json()
  assert data["message"]
  # assert data["message"] == "succeed"

def test_put_metrics():
  '''
  put method is not needed, should be failed 
  
  '''
  response = requests.put(url_metrics)
  data = response.json()
  assert data["failed"]
  assert data["failed"] == "method not required"


def test_unknown_sensor_metrics():
  '''
  valid metrics data should be ingested
  '''
  response = requests.post(url_metrics, json=MetricsData.unknown_sensor_metrics)
  data = response.json()
  assert data["failed"]
  assert data["failed"] == "Unknown sensor found"
