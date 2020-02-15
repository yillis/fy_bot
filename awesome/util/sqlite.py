import sqlite3
import contextlib
import pickle
import awesome.util.const as const


class _SQLClient(object):
    """
    the DB struct is (name text primary key not null, data blob, method str)
    where is [(keyword, weight),]
    """

    def __init__(self, tb_name: str):
        self._tb_name = tb_name

    @contextlib.asynccontextmanager
    async def _connect(self):
        self._conn = sqlite3.connect(self._tb_name)
        self._cursor = self._conn.cursor()
        yield
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    async def data_query(self, problem_name: str = None):
        async with self._connect():
            if problem_name:
                self._cursor.execute("""SELECT data FROM %s WHERE name=%s""" % (self._tb_name, problem_name))

    async def method_update(self, problem_name: str, method: str):
        async with self._connect():
            self._cursor.execute("""INSERT OR IGNORE INTO %s (name) VALUES (%s)""" % (self._tb_name, problem_name))
            self._cursor.execute("""ALTER %s SET method=%s WHERE name=%s""" % (self._tb_name, method, problem_name))


async def get_data() -> list:
    sql_client = _SQLClient(const.PROBLEM_DB_NAME)
    data = _SQLClient.data_query()

    dic = {}
    for i in data:
        keyword_and_weight = pickle.loads(i)
        for keyword, weight in keyword_and_weight:
            if text.find(keyword) != -1:



async def get_problem_name(text: str):


async def get_method(problem_name: str) -> str:


async def update_method(problem_name: str, method: str):
