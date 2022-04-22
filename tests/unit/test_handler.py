import json
import pytest

from reports import app

import requests
from assertpy.assertpy import assert_that


@pytest.fixture()
def fixture_todoitems_event():
    return {
        "eventType": "todoitems",
        "pathParameters": { }
    }


@pytest.fixture()
def fixture_todoitems_byid_event():
    return {
        "eventType": "todoitems",
        "pathParameters": {
            "Id": 2
        }
    }


@pytest.fixture()
def fixture_locations_event():
    return {
        "eventType": "locations",
        "pathParameters": { }
    }


@pytest.fixture()
def fixture_locations_byid_event():
    return {
        "eventType": "locations",
        "pathParameters": {
            "Id": 1400
        }
    }


@pytest.fixture()
def fixture_users_event():
    return {
        "eventType": "users",
        "pathParameters": { }
    }


@pytest.fixture()
def fixture_users_byid_event():
    return {
        "eventType": "users",
        "pathParameters": {
            "Id": 1
        }
    }


class TestReportsGetAPI:
    def test_lambda_handler_todoitems(self, fixture_todoitems_event):
        ret = app.lambda_handler(fixture_todoitems_event, "")
        data = json.loads(ret["body"])

        assert_that(ret["statusCode"]).is_equal_to(requests.codes.ok)
        assert_that(data["data"]).is_length(5)
        # assert_that(data["data"]).extracting("name").contains("Feed Fish")
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "Success"

    def test_lambda_handler_todoitems_byid(self, fixture_todoitems_byid_event):
        ret = app.lambda_handler(fixture_todoitems_byid_event, "")
        data = json.loads(ret["body"])

        assert_that(ret["statusCode"]).is_equal_to(requests.codes.ok)
        assert_that(data["data"]["name"]).is_equal_to("Feed Fish")
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "Success"

    def test_lambda_handler_locations(self, fixture_locations_event):
        ret = app.lambda_handler(fixture_locations_event, "")
        data = json.loads(ret["body"])

        assert_that(ret["statusCode"]).is_equal_to(requests.codes.ok)
        assert_that(data["data"]).is_length(7)
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "Success"

    def test_lambda_handler_locations_byid(self, fixture_locations_byid_event):
        ret = app.lambda_handler(fixture_locations_byid_event, "")
        data = json.loads(ret["body"])

        assert_that(ret["statusCode"]).is_equal_to(requests.codes.ok)
        assert_that(data["data"]["street_address"]).is_equal_to("2014 Jabberwocky Rd")
        assert_that(data["data"]["city"]).is_equal_to("Southlake")
        assert_that(data["data"]["state_province"]).is_equal_to("Texas")
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "Success"

    def test_lambda_handler_users(self, fixture_users_event):
        ret = app.lambda_handler(fixture_users_event, "")
        data = json.loads(ret["body"])

        assert_that(ret["statusCode"]).is_equal_to(requests.codes.ok)
        assert_that(data["data"]).is_length(4)
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "Success"

    def test_lambda_handler_users_byid(self, fixture_users_byid_event):
        ret = app.lambda_handler(fixture_users_byid_event, "")
        data = json.loads(ret["body"])

        assert_that(ret["statusCode"]).is_equal_to(requests.codes.ok)
        assert_that(data["data"]["firstname"]).is_equal_to("Freddy")
        assert_that(data["data"]["lastname"]).is_equal_to("Benson")
        assert_that(data["data"]["username"]).is_equal_to("freddy")
        assert_that(data["data"]["email"]).is_equal_to("fbenson@jackal.com")
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "Success"
