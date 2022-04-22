import psycopg2


class Database:
    credentials = {"host": '<host>', "database": '<database>', "user": '<user>', "password": '<password>'}

    def __init__(self):
        self._conn = psycopg2.connect(**self.credentials)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def query_one(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchone()
