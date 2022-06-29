import logging
from http import HTTPStatus
from typing import Union, List

import snowflake.connector
import ujson
from cyberark_api.cyberark_client import CyberArkClient

from src.common.api_exception import ApiException
from src.common.credentials import Credentials
from src.common.db_client import DbClient
from src.cvms.customer_vehicle_snapshot import CustomerVehicleSnapshot
from src.cvms.types.endpoint_type import EndpointType

# CyberArk Settings
CYBER_ARK_APP_ID = "dev-snowflake"
CYBER_ARK_SAFE = "AWS-DEV-DB-SNOWFLAKE"
CYBER_ARK_OBJ_NAME = "DEV_DATASERVICES_DB-snowflake-API_DEV"
# Snowflake Settings
SNOWFLAKE_ACCOUNT = "efleets-dataservices.privatelink"
SNOWFLAKE_DB = "DEV_DATASERVICES_DB"
SNOWFLAKE_ROLE = "DEV_API_SERVICE"


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    try:
        db_connection = get_db_connection(get_credentials())
        db_client = DbClient(db_connection)
        data = retrieve_event_data(db_client, event)
        if data:
            return success_response(HTTPStatus(200), data)
        else:
            return error_response(HTTPStatus(404), "No data was found", HTTPStatus(404).description)

    except Exception as err:
        return error_response(HTTPStatus(400), "Something went wrong. Unable to query resource", str(err))


def success_response(status: HTTPStatus, data: List):
    return {
        "statusCode": status.value,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": ujson.dumps({
            "message": "Success",
            "data": data
        })
    }


def error_response(status: HTTPStatus, message: str, error: str):
    return {
        "statusCode": status.value,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": ujson.dumps({
            "message": message,
            "error": error
        })
    }


def retrieve_event_data(db_client: DbClient, event) -> list:
    result: list = []
    event_type = event.get("eventType")
    object_id = event["pathParameters"].get("id")

    if event_type and object_id:
        query = get_query()
        if event_type == EndpointType.customers:
            result = CustomerVehicleSnapshot(db_client, query).read_customers(object_id)
        elif event_type == EndpointType.vehicles:
            id_type = event["queryStringParameters"].get("idtype")
            result = CustomerVehicleSnapshot(db_client, query).read_vehicles(object_id, id_type)

    return result


def get_query() -> str:
    # TODO: Read query from aws s3 bucket instead
    sql_file = open("query.sql")
    return sql_file.read()


def get_credentials() -> Credentials:
    # Credentials specific provider (i.e., cyberark) is defined below
    client = CyberArkClient()

    account = client.get_account(CYBER_ARK_APP_ID, CYBER_ARK_SAFE, CYBER_ARK_OBJ_NAME)

    return Credentials(account)


def get_db_connection(creds: Credentials):
    # DB specific connector (i.e., snowflake) is defined below
    try:
        conn = snowflake.connector.connect(
            user=creds.username,
            password=creds.password,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DB,
            role=SNOWFLAKE_ROLE)

        return conn
    except Exception as e:
        error_message = f"Unable to retrieve Snowflake secret and/or instantiating Snowflake class: {str(e)}"
        raise ApiException(error_message, "establish_snowflake_conn")
