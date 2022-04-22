import psycopg2
import ujson

from .utils.db import Database


def lambda_handler(event, context):
    try:
        event_type = event["eventType"]
    except TypeError:
        event_type = None
    except KeyError:
        event_type = None

    try:
        object_id = event["pathParameters"]["Id"]
    except TypeError:
        object_id = None
    except KeyError:
        object_id = None

    try:
        return {
            "statusCode": 200,
            "body": ujson.dumps({
                "message": "Success",
                "data": retrieve_event_data(event_type, object_id)
            })
        }
    except Exception as err:
        return {
            "statusCode": 400,
            "body": ujson.dumps({
                "message": "Something went wrong. Unable to parse data !",
                "error": str(err)
            })
        }


def retrieve_event_data(event_type, object_id):
    if event_type == "todoitems":
        return retrieve_todo_info(object_id)
    elif event_type == "locations":
        return retrieve_location_info(object_id)
    elif event_type == "users":
        return retrieve_user_info(object_id)


def retrieve_todo_info(todo_id):
    base_query = "SELECT * FROM todoitems"
    result = list()

    with Database() as db:
        if todo_id is not None:
            query = base_query + " WHERE id = %(id)s"
            # retrieve particular object from db.
            try:
                todoitem = db.query_one(query, {'id': todo_id})
                if todoitem is None:
                    return {"error": "The respective id does not exist !"}

            except (Exception, psycopg2.Error) as error:
                return {"error": "Please provide a valid ObjectId. Error is " + error}

            return {
                'id': todo_id,
                'name': todoitem[1],
                'description': todoitem[2],
                'complete': todoitem[3]
            }
        else:
            # retrieve all information from db
            rows = db.query(base_query)
            for record in rows:
                result.append(record)

            return result


def retrieve_location_info(location_id):
    base_query = "SELECT * FROM locations l " \
                 "JOIN countries c ON l.country_id = c.country_id " \
                 "JOIN regions r ON c.region_id = r.region_id"
    result = list()

    with Database() as db:
        if location_id is not None:
            # retrieve particular object from db.
            query = base_query + " WHERE location_id = %(location_id)s"
            try:
                location = db.query_one(query, {'location_id': location_id})
                if location is None:
                    return {"error": "The respective id does not exist !"}

            except (Exception, psycopg2.Error) as error:
                return {"error": "Please provide a valid ObjectId. Error is " + error}

            return {
                'location_id': location_id,
                'street_address': location[1],
                'postal_code': location[2],
                'city': location[3],
                'state_province': location[4],
                'country_name': location[7],
                'region_name': location[10]

            }
        else:
            # retrieve all information from db
            rows = db.query(base_query)
            for record in rows:
                result.append(record)

            return result


def retrieve_user_info(user_id):
    base_query = "SELECT * FROM users"
    result = list()

    with Database() as db:
        if user_id is not None:
            query = base_query + " WHERE id = %(id)s"
            # retrieve particular object from db.
            try:
                user = db.query_one(query, {'id': user_id})
                if user is None:
                    return {"error": "The respective id does not exist !"}

            except (Exception, psycopg2.Error) as error:
                return {"error": "Please provide a valid ObjectId. Error is " + error}

            return {
                'id': user_id,
                'firstname': user[1],
                'lastname': user[2],
                'email': user[3],
                'username': user[4]
            }
        else:
            # retrieve all information from db
            rows = db.query(base_query)
            for record in rows:
                result.append(record)

            return result
