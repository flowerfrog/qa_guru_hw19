import json
from datetime import datetime
import datetime
import jsonschema
import requests
from tests.utils import load_schema


def test_get_list_resource_successfully():
    url = "https://reqres.in/api/unknown"
    schema = load_schema('get_list_resource.json')

    result = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_get_single_resource_successfully():
    url = "https://reqres.in/api/unknown/2"
    schema = load_schema('get_single_resource.json')

    result = requests.get(url)

    assert result.status_code == 200
    assert result.json()['data']['id'] == 2
    jsonschema.validate(result.json(), schema)


def test_get_single_resource_not_found():
    url = "https://reqres.in/api/unknown/23"
    schema = load_schema('get_single_resource_not_found.json')

    result = requests.get(url)

    assert result.status_code == 404
    jsonschema.validate(result.json(), schema)


def test_post_create_user_successfully():
    url = "https://reqres.in/api/users"
    schema = load_schema('post_create_user.json')

    result = requests.post(url, {
        "name": "morpheus",
        "job": "leader"
    })

    assert result.status_code == 201
    assert result.json()["name"] == "morpheus"
    assert result.json()["job"] == "leader"
    jsonschema.validate(result.json(), schema)


def test_post_register_unsuccessful():
    url = "https://reqres.in/api/register"
    schema = load_schema('post_register_unsuccessful.json')

    result = requests.post(url, {
        "email": "sydney@fife",
        "password": "",
    })

    assert result.status_code == 400
    assert result.json()["error"] == "Missing password"
    jsonschema.validate(result.json(), schema)


def test_post_register_successful():
    url = "https://reqres.in/api/register"
    schema = load_schema('post_register_successful.json')

    result = requests.post(url, {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    })

    assert result.status_code == 200
    assert result.json()["id"] == 4
    assert result.json()["token"] is not None
    jsonschema.validate(result.json(), schema)


def test_put_update_user_successful():
    url = "https://reqres.in/api/users/2"
    schema = load_schema('put_update_user.json')
    result = requests.put(url, {
        "name": "morpheus",
        "job": "zion resident"
    })
    formatted_datetime = datetime.datetime.utcnow().isoformat(timespec='seconds')
    json_datetime = json.loads(json.dumps(formatted_datetime))

    assert result.status_code == 200
    assert result.json()["name"] == "morpheus"
    assert result.json()["job"] == "zion resident"
    assert json_datetime in result.json()["updatedAt"]
    jsonschema.validate(result.json(), schema)


def test_delete_user_successful():
    url = "https://reqres.in/api/users/2"

    result = requests.delete(url)

    assert result.status_code == 204


def test_post_login_successful():
    url = "https://reqres.in/api/login"
    schema = load_schema('post_login_user.json')

    result = requests.post(url, {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })

    assert result.status_code == 200
    assert result.json()["token"] is not None
    jsonschema.validate(result.json(), schema)


def test_post_login_unsuccessful():
    url = "https://reqres.in/api/login"
    schema = load_schema('post_register_unsuccessful.json')

    result = requests.post(url, {
        "email": "eve.holt@reqres.in",
        "password": ""
    })

    assert result.status_code == 400
    assert result.json()["error"] == "Missing password"
    jsonschema.validate(result.json(), schema)
