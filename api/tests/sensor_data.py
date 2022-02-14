
class SensorData(object):
    
    one_unique_sensor = {
        "id":"85",
        "city": "dublin",
        "country": "ireland"
    }

    one_duplicate_sensor = {
        "id":"85",
        "city": "dublin",
        "country": "ireland"
    }

    invalid_id_sensor = {
        "id":"hi",
        "city": "dublin",
        "country": "ireland"
    }

    invalid_city_sensor = {
    "id":"86",
        "city": 1,
        "country": "ireland"
    }

    only_id_sensor = {
        "id": "87"
    }