from urllib import response
from sensor_data import SensorData
import pytest
import requests



# The root url of the flask api to get the sensor details
# eg http://127.0.0.1:5000/iot/api/v1.0/sensors/82
url_sensor = 'http://127.0.0.1:5000/iot/api/v1.0/sensors'


def test_post_unknown_sensor():

    '''
     posting a sensor is not reuiqred as sensor manger api is available to post sensor(s)
    '''
    response = requests.post(url_sensor + "/100", json=SensorData.only_id_sensor)
    data = response.json()
    assert data["failed"]
    assert data["failed"] == "method not required"


def test_get_known_sensor():

    '''
     On requesting known sensor, response should not be null, a sensor is returned
    '''
    response = requests.get(url_sensor + "/82")
    data = response.json()
    assert data['id']
    assert data['id'] == 82


def test_post_sensor():
    '''
         On requesting unknown sensor, response should be empty
    '''
    response = requests.get(url_sensor + "/820")
    data = response.json()
    assert data == {}


def test_delete_known_sensor():
    '''
        deleting an available sensor should be succeed
    '''
    response = requests.delete(url_sensor + "/82")
    data = response.json()
    assert data["message"]
    assert data["message"] == "succeed"

def test_unknown_sensor():
    '''
    deleting an unknow sensor should be failed
    '''
    response = requests.delete(url_sensor + "/820")
    data = response.json()
    assert data['failed']
    assert data['failed'] == "no record found"

