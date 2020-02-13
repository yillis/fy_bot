import sqlite3
import contextlib


class SQLClient(object):
    def __init__(self, db_name: str):
        self._db_name = db_name

    @contextlib.asynccontextmanager
    async def _connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()
        yield
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    async def query(self, table_name: str):
        async with self._connect():
            return self._cursor.execute("""SELECT * FROM %s""" % table_name)

    async def problem_update(self):
        async with self._connect():
