from __future__ import annotations

from src.common.api_exception import ApiException
from src.common.db_client import DbClient
from src.cvms.types.vehicle_id_type import VehicleIdType


class CustomerVehicleSnapshot(object):
    def __init__(self, db_client: DbClient, query: str):
        self._db_client = db_client
        self._query = query

    def read_customers(self, customer_id: str):
        customer_vehicle_list = self.run_db_query(self._query, self._db_client, customer_id, "MASTER_CUSTOMER_NUMBER")
        print(customer_vehicle_list)

        return customer_vehicle_list

    def read_vehicles(self, vehicle_id: str, id_type: VehicleIdType) -> list:
        if id_type == VehicleIdType.vehicleId:
            customer_vehicle_list = self.run_db_query(self._query, self._db_client, vehicle_id, "VEHICLE_ID")
        elif id_type == VehicleIdType.unitNumber:
            customer_vehicle_list = self.run_db_query(self._query, self._db_client, vehicle_id, "UNIT_NUMBER")
        elif id_type == VehicleIdType.quoteNumber:
            customer_vehicle_list = self.run_db_query(self._query, self._db_client, vehicle_id, "QUOTE_NUMBER")
        elif id_type == VehicleIdType.vin:
            customer_vehicle_list = self.run_db_query(self._query, self._db_client, vehicle_id, "VIN")
        else:
            customer_vehicle_list = []
        print(customer_vehicle_list)

        return customer_vehicle_list

    def run_db_query(self, query: str, db_client: DbClient, obj_id: str, filter_col: str) -> list[tuple] | list[dict]:
        # TODO: Paramertize limit variable
        limit = 20
        try:
            if not obj_id and not filter_col:
                data_sql = f"""SELECT * FROM ({query}) AS api_query WHERE 1=1 LIMIT {limit}"""
            else:
                data_sql = f"""SELECT * FROM ({query}) AS api_query WHERE {filter_col} = '{obj_id}' LIMIT {limit}"""

            return db_client.query(data_sql)

        except Exception as e:
            error_message = f"Unable to retrieve data: " + str(e)
            raise ApiException(error_message, "run_db_query")
        finally:
            if db_client.connection:
                db_client.close()
