
from urllib import response
from sensors_data import SensorData
import pytest
import requests

# The root url of the flask api
url = 'http://127.0.0.1:5000/iot/api/v1.0/sensors' 

def test_delete_empty_table():
  '''
    Initially sensors table should be empty. 
    On deleting records, it shoudl throw a message
    {"failed": "no record found"}
  '''
  response = requests.delete(url)
  data = response.json()
  assert data["failed"]
  assert data["failed"] == "no record found"

def test_register_new_sensors():
  '''
  list of sensors should be accepted sensors with unique Ids for the registration
  '''

  response = requests.post(url, json=SensorData.new_sensors)
  data = response.json()
  assert data["message"]
  assert data["message"] == "succeed"


def test_register_duplicate_sensors():
  '''
    sensors table should not accept duplicate sensor(s) for the registration. 
    entire transction should be failed. 
  '''
  response = requests.post(url, json=SensorData.duplicate_sensors)
  data = response.json()
  assert data["failed"]
  assert data["failed"] == "duplicate sensor or missing k/v pairs"

def test_register_one_sensor():
  '''
  one sensor should be accepted with unique Id for the registration
  '''
  response = requests.post(url, json=SensorData.one_unique_sensor)
  data = response.json()
  assert data["message"]
  assert data["message"] == "succeed"


def test_register_one_sensor():
  '''
  one sensor should not be accepted with duplicate Id for the registration
  '''
  response = requests.post(url, json=SensorData.one_duplicate_sensor)
  data = response.json()
  assert data["message"]
  assert data["message"] == "succeed"
   
def test_invalid_sensor():
  '''
  sensor should should have a valid id, should be an integer
  '''
  response = requests.post(url, json=SensorData.invalid_id_sensor)
  data = response.json()
  assert data["failed"]
 
def test_invalid_city_sensor():
  '''
  sensor should should have a valid country/city, should be a String
  '''
  response = requests.post(url, json=SensorData.invalid_city_sensor)
  data = response.json()
  assert data["failed"]

def test_only_id_sensor():
  '''
  one sensor should not be accepted with duplicate Id for the registration
  '''
  response = requests.post(url, json=SensorData.only_id_sensor)
  data = response.json()
  assert data["message"]
  assert data["message"] == "succeed"

def test_get_sensors():

    '''
     On requesting sensors, response should not be null as array sensors are returned
    '''
    response = requests.post(url, json=SensorData.only_id_sensor)
    data = response.json()
    assert data is not None
    assert len(data) > 0
  