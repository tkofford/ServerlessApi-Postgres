import sqlite3

import pytest
from assertpy.assertpy import assert_that

from src.common.db_client import DbClient
from src.cvms.customer_vehicle_snapshot import CustomerVehicleSnapshot
from src.cvms.types.vehicle_id_type import VehicleIdType


@pytest.fixture
def db():
    # Fixture to set up the in-memory database with test data
    db_client = DbClient(sqlite3.connect(":memory:"))
    yield db_client
    db_client.close()


@pytest.fixture
def setup_db(db):
    # Create a DB table
    ddl_file = open("data/create_table.sql", "r")
    create_table_query = ddl_file.read()
    db.execute(create_table_query)

    # Populate the DB table with data
    data_file = open("data/testdata.txt", "r")
    lines = data_file.readlines()
    data = [tuple(line.strip().split(", ")) for line in lines]
    print(data[0])
    db.executemany("INSERT INTO cvms VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                   "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    db.commit()


@pytest.mark.usefixtures("setup_db")
def test_read_customers_by_customer_id(db):
    # bucket_name = "my-test-bucket"
    # # Set up a mock S3 bucket & add an sql file to it
    # s3_client.create_bucket(Bucket=bucket_name)
    # resource_child = "vehicle-series-summary"
    # object_key = f"inbound/api/data/{resource_child}.sql"
    # query = "SELECT * FROM cvms"
    # s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=query)
    #
    # # Test the lambda function
    # my_s3_client = S3Client(AWS_REGION)
    # resource = ResourceObject("api", "data", resource_child, "*")
    # query_str = get_query(my_s3_client, bucket_name, resource)

    query_str = "SELECT * FROM cvms"
    rows = CustomerVehicleSnapshot(db, query_str).read_customers("255105")
    # Test to make sure that there are 20 items in the database
    # rows = list(db.execute(query))
    assert_that(rows).is_length(20)
    # Check first row for expected customer data
    customer = rows[0]
    assert_that(customer).contains('Big Ass Fans', 'Fleet', 'Equity Lease - Fixed')



@pytest.mark.usefixtures("setup_db")
def test_read_vehicles_by_vehicle_id(db):
    query_str = "SELECT * FROM cvms"
    rows = CustomerVehicleSnapshot(db, query_str).read_vehicles("1962356", VehicleIdType.vehicleId)
    # Test specific vehicle attributes
    assert_that(rows).is_length(1)
    vehicle = rows[0]
    assert_that(vehicle).contains('Big Ass Fans', 'Ford', 'F-150', '1/2 Ton Pickup Ext 4x2')


@pytest.mark.usefixtures("setup_db")
def test_read_vehicles_by_vin(db):
    query_str = "SELECT * FROM cvms"
    rows = CustomerVehicleSnapshot(db, query_str).read_vehicles("1FD7X2A69HED33008", VehicleIdType.vin)
    # Test specific vehicle attributes
    assert_that(rows).is_length(1)
    vehicle = rows[0]
    assert_that(vehicle).contains('Big Ass Fans', 'Ford', 'F-250', '3/4 Ton Pickup Ext 4x2')


@pytest.mark.usefixtures("setup_db")
def test_read_vehicles_by_vin(db):
    query_str = "SELECT * FROM cvms"
    rows = CustomerVehicleSnapshot(db, query_str).read_vehicles("6022062", VehicleIdType.quoteNumber)
    # Test specific vehicle attributes
    assert_that(rows).is_length(1)
    vehicle = rows[0]
    assert_that(vehicle).contains('Big Ass Fans', 'Toyota', 'Camry', 'Full-size Sedan')


@pytest.mark.usefixtures("setup_db")
def test_read_vehicles_by_vin(db):
    query_str = "SELECT * FROM cvms"
    rows = CustomerVehicleSnapshot(db, query_str).read_vehicles("256342", VehicleIdType.unitNumber)
    # Test specific vehicle attributes
    assert_that(rows).is_length(1)
    vehicle = rows[0]
    assert_that(vehicle).contains('Big Ass Fans', 'Ford', 'Escape', 'Compact SUV 4x4')
