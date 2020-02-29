import sqlite3
import contextlib
import pickle

_TB_NAME = 'repair_msg'
_DB_NAME = 'fybot.db'


class _SQLClient(object):
    """
    the DB struct is (name text primary key not null, data blob, method str)
    data: [(keyword, weight = 1),]
    """

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

    async def data_query(self, tb_name):
        async with self._connect():
            print('error')
            # try:
            data = self._cursor.execute("""SELECT name, data FROM %s""" % tb_name)
            # except sqlite3.OperationalError as err:
            #    return []
            res = {}
            for i in data:
                if i[1]:
                    tmp = pickle.loads(i[1])
                    res[i[0]] = tmp
            print(res)
            return res

    async def method_query(self, problem: str, tb_name) -> str:
        async with self._connect():
            method = self._cursor.execute("""SELECT method FROM %s WHERE name = '%s'""" % (tb_name, problem))
            try:
                return next(method)[0]
            except StopIteration:
                return ""

    async def method_update(self, problem: str, method: str, tb_name):
        async with self._connect():
            self._cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (name text primary key not null, data blob, method str)""" % tb_name)
            self._cursor.execute("""INSERT OR IGNORE INTO %s (name) VALUES ('%s')""" % (tb_name, problem))
            self._cursor.execute("""UPDATE %s SET method='%s' WHERE name='%s'""" % (tb_name, method, problem))

    async def show_problems(self, tb_name):
        async with self._connect():
            return list(self._cursor.execute("""SELECT name FROM %s""" % tb_name))

    async def data_update(self, problem, data, tb_name):
        async with self._connect():
            self._cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (name text primary key not null, data blob, method str)""" % tb_name)
            self._cursor.execute(
                """REPLACE INTO %s (name, data) VALUES (?,?) """ % tb_name,
                (problem, pickle.dumps(data, protocol=0),))

    async def get_data(self, problem, tb_name) -> list:
        async with self._connect():
            try:
                return pickle.loads(
                    next(self._cursor.execute("""SELECT data FROM %s WHERE name = '%s'""" % (tb_name, problem)))[0])
            except StopIteration as err:
                return []


# for ask
async def get_ask_problem(text: str) -> str:
    data = await get_ask_data()
    print(data)
    dic = {}
    for problem in data:
        for keyword in data[problem]:
            if text.find(keyword) != -1:
                weight = 1
                dic[problem] = dic.get(problem, 0) + weight
    return '' if len(dic) == 0 else max(dic, key=dic.get)


async def get_method(problem: str) -> str:
    sqlite = _SQLClient(_DB_NAME)
    return await sqlite.method_query(problem, _TB_NAME)


async def get_problem_and_method(text: str) -> (str, str):
    keywords = get_update_keyword()
    for keyword in keywords:
        index = text.find(keyword)
        if index != -1:
            return text[0:index], text[index + len(keyword):]
    return '', ''


async def update_method(problem: str, method: str):
    sqlite = _SQLClient(_DB_NAME)
    await sqlite.method_update(problem, method, _TB_NAME)


# interface
async def get_ask_data():
    sqlite = _SQLClient(_DB_NAME)
    return await sqlite.data_query(_TB_NAME)


async def get_update_keyword():
    return ['的解决方法是', '的方法是']


async def get_ask_keyword():
    sqlite = _SQLClient(_DB_NAME)
    return await sqlite.show_problems(_TB_NAME)


async def add_keyword(problem: str, keyword: str):
    keywords = await get_keywords(problem)
    print(keywords)
    if keyword not in keywords:
        keywords.append(keyword)
    sqlite = _SQLClient(_DB_NAME)
    await sqlite.data_update(problem, keywords, _TB_NAME)


# async def del_keyword


async def get_keywords(problem: str) -> list:
    sqlite = _SQLClient(_DB_NAME)
    return await sqlite.get_data(problem, _TB_NAME)
