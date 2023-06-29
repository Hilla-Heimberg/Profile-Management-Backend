import json

import requests
import unittest

from social_profile_server.query_executor import execute_update

CREATE_ENDPOINT = "http://127.0.0.1:5000/create/"
UPDATE_ENDPOINT = "http://127.0.0.1:5000/update/"
GET_ENDPOINT = "http://127.0.0.1:5000/get/"
DELETE_ENDPOINT = "http://127.0.0.1:5000/delete/"

VALID_PROFILE_1 = {
    "username": "omrimar",
    "first_name": "omri",
    "last_name": "marom",
    "email": "omri@copenhagen",
    "profile_image": "C:\\Users\\97250\\Pictures\\Screenshots\\Screenshot (1).png"
}

PARTIAL_PROFILE_1 = {
    "username": "omrimar"
}


UPDATED_PROFILE_1 = {
    "username": "omrimar",
    "first_name": "marom",
    "last_name": "omri",
    "email": "omri@paris",
    "profile_image": "C:\\Users\\97250\\Pictures\\Screenshots\\Screenshot (1).png"
}

VALID_PROFILE_2 = {
    "username": "hilla_heimberg",
    "first_name": "hilla",
    "last_name": "heimberg",
    "email": "hilla@london",
    "profile_image": "C:\\Users\\97250\\Pictures\\Screenshots\\Screenshot (1).png"
}

PARTIAL_PROFILE_2 = {
    "username": "hilla_heimberg",
    "first_name": "hilla",
    "last_name": "heimberg",
    "email": "hilla@london",
}

UPDATED_PROFILE_2 = {
    "username": "hilla_heimberg",
    "first_name": "Hilla",
    "last_name": "Heimberg",
    "email": "hilla@israel",
    "profile_image": "C:\\Users\\97250\\Pictures\\Screenshots\\Screenshot (1).png"
}

PROFILE_WITH_INVALID_IMAGE = {
    "username": "hilla_heimberg",
    "first_name": "hilla",
    "last_name": "heimberg",
    "email": "hilla@london",
    "profile_image": "invalid"
}


class TestSocialProfileServerEndpoints(unittest.TestCase):

    def setUp(self) -> None:
        execute_update(
            f"DELETE "
            f"FROM profiles "
        )

    # -----------------------------------------------------------------------------------------------------------------
    # tests for /create/ endpoint
    def test_create_with_valid_parameters(self):
        r = requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        assert r.status_code == 201

        r = requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_2)
        assert r.status_code == 201

    def test_create_with_existing_username(self):
        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        r = requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        assert r.status_code == 400
        assert r.text == "User already exists, try to login"

    def test_create_with_missing_parameter(self):
        r = requests.post(url=CREATE_ENDPOINT, data=PARTIAL_PROFILE_1)
        assert r.status_code == 400
        assert r.text == "Invalid request body"

        r = requests.post(url=CREATE_ENDPOINT, data=PARTIAL_PROFILE_2)
        assert r.status_code == 400
        assert r.text == "Invalid request body"

    # -----------------------------------------------------------------------------------------------------------------
    # tests for /update/ endpoint
    def test_update_with_valid_parameters(self):
        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        r = requests.put(url=UPDATE_ENDPOINT, data=UPDATED_PROFILE_1)
        assert r.status_code == 200

        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_2)
        r = requests.put(url=UPDATE_ENDPOINT, data=UPDATED_PROFILE_2)
        assert r.status_code == 200

    def test_update_with_no_existing_username(self):
        r = requests.put(url=UPDATE_ENDPOINT, data=UPDATED_PROFILE_1)
        assert r.status_code == 400
        assert r.text == "User not found, try again"

        r = requests.put(url=UPDATE_ENDPOINT, data=UPDATED_PROFILE_2)
        assert r.status_code == 400
        assert r.text == "User not found, try again"

    def test_update_with_missing_parameter(self):
        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        r = requests.put(url=UPDATE_ENDPOINT, data=PARTIAL_PROFILE_1)
        assert r.status_code == 400
        assert r.text == "Invalid request body"

        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_2)
        r = requests.put(url=UPDATE_ENDPOINT, data=PARTIAL_PROFILE_2)
        assert r.status_code == 400
        assert r.text == "Invalid request body"

    # -----------------------------------------------------------------------------------------------------------------
    # tests for /delete/ endpoint
    def test_delete_with_valid_parameters(self):
        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        r = requests.put(url=DELETE_ENDPOINT, data=VALID_PROFILE_1)
        assert r.status_code == 200

        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_2)
        r = requests.put(url=DELETE_ENDPOINT, data=PARTIAL_PROFILE_2)
        assert r.status_code == 200

    def test_delete_with_no_existing_username(self):
        r = requests.put(url=DELETE_ENDPOINT, data=PARTIAL_PROFILE_1)
        assert r.status_code == 400
        assert r.text == "User not found, try again"

        r = requests.put(url=DELETE_ENDPOINT, data=VALID_PROFILE_2)
        assert r.status_code == 400
        assert r.text == "User not found, try again"

    # -----------------------------------------------------------------------------------------------------------------
    # tests for /get/ endpoint
    def test_get_with_valid_parameters(self):
        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        r = requests.get(url=GET_ENDPOINT, data=PARTIAL_PROFILE_1)
        assert r.status_code == 200
        assert r.text == json.dumps(dict(VALID_PROFILE_1), indent=4)

        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_2)
        r = requests.get(url=GET_ENDPOINT, data=PARTIAL_PROFILE_2)
        assert r.status_code == 200
        assert r.text == json.dumps(dict(VALID_PROFILE_2), indent=4)

    def test_get_with_no_existing_username(self):
        r = requests.get(url=GET_ENDPOINT, data=PARTIAL_PROFILE_1)
        assert r.status_code == 400
        assert r.text == "User not found, try again"

        r = requests.get(url=GET_ENDPOINT, data=VALID_PROFILE_2)
        assert r.status_code == 400
        assert r.text == "User not found, try again"

    def test_get_with_no_existing_image(self):
        requests.post(url=CREATE_ENDPOINT, data=PROFILE_WITH_INVALID_IMAGE)
        r = requests.get(url=GET_ENDPOINT, data=PROFILE_WITH_INVALID_IMAGE)
        assert r.status_code == 400
        assert r.text == "Profile image not found"

    def test_get_with_updated_profile(self):
        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_1)
        requests.put(url=UPDATE_ENDPOINT, data=UPDATED_PROFILE_1)
        r = requests.get(url=GET_ENDPOINT, data=PARTIAL_PROFILE_1)
        assert r.status_code == 200
        assert r.text == json.dumps(dict(UPDATED_PROFILE_1), indent=4)

        requests.post(url=CREATE_ENDPOINT, data=VALID_PROFILE_2)
        requests.put(url=UPDATE_ENDPOINT, data=UPDATED_PROFILE_2)
        r = requests.get(url=GET_ENDPOINT, data=UPDATED_PROFILE_2)
        assert r.status_code == 200
        assert r.text == json.dumps(dict(UPDATED_PROFILE_2), indent=4)


if __name__ == '__main__':
    unittest.main()
