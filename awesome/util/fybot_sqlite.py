import sqlite3
import contextlib
import pickle

_TB_NAME = 'repair_msg'
_DB_NAME = 'fybot.db'


class SQLClient(object):
    """
    this client is used to deal with the 'fy ask and answer' features
    the command now have:
    1.ask
    2.update
    3.add
    the operation of DB, if you want to connect the db, please use _connect() func
    the DB struct is (name text primary key not null, data blob, method str)
    data: [(keyword, weight = 1),]
    """

    def __init__(self, db_name: str = _DB_NAME, tb_name: str = _TB_NAME):
        self._db_name = db_name
        self._tb_name = tb_name

    @contextlib.asynccontextmanager
    async def _connect(self):
        """
        connect to the db
        :return:
        """
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS %s (name text primary key not null, data blob, method str)""" % self.tb_name)
        yield
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    async def name_and_data_query(self) -> dict:
        """
        query the name and data
        :return: a dict {name: data}
        """
        async with self._connect():
            data = self._cursor.execute("""SELECT name, data FROM %s""" % self._tb_name)
            res = {}
            for i in data:
                if i[1]:
                    tmp = pickle.loads(i[1])
                    res[i[0]] = tmp
            return res

    async def method_query(self, problem: str) -> str:
        """
        query the method of the problems in tb
        :param problem: problem names
        :return: the method
        """
        async with self._connect():
            method = self._cursor.execute("""SELECT method FROM %s WHERE name = '%s'""" % (self._tb_name, problem))
            try:
                return next(method)[0]
            except StopIteration:
                return ""

    async def method_update(self, problem: str, method: str):
        """
        update the method of the problems in tb
        :param problem: problem names
        :param method: the new method you want to update
        """
        async with self._connect():
            self._cursor.execute("""INSERT OR IGNORE INTO %s (name) VALUES ('%s')""" % (self._tb_name, problem))
            self._cursor.execute("""UPDATE %s SET method='%s' WHERE name='%s'""" % (self._tb_name, method, problem))

    async def show_problems(self) -> list:
        """
        to show all problems the tb have
        :return: a problems list
        """
        async with self._connect():
            problems = self._cursor.execute("""SELECT name FROM %s""" % self._tb_name)
            res = []
            for problem in problems:
                res.append(problem[0])
            return res

    async def data_update(self, problem, data):
        """
        update the data of the problem in tb
        :param problem: problem names
        :param data: the data you want to update to the tb
        """
        async with self._connect():
            self._cursor.execute(
                """REPLACE INTO %s (name, data) VALUES (?,?) """ % self._tb_name,
                (problem, pickle.dumps(data, protocol=0),))

    async def get_data(self, problem) -> list:
        """
        query a data of problem
        :param problem: problems
        :return: data as a list
        """
        async with self._connect():
            try:
                return pickle.loads(
                    next(self._cursor.execute("""SELECT data FROM %s WHERE name = '%s'""" % (self._tb_name, problem)))[
                        0])
            except StopIteration as err:
                return []
