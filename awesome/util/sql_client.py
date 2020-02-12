"""
in this module
you can connect to the remote SQL DB

until now
you can query and update the table in the database
"""
# standard module
import contextlib

# extend module
import pymysql

# project module
import config


class SQLClient(object):
    def __init__(self, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD,
                 charset=config.DB_CHARSET):
        """
        init the essential member in this class
        :param host: the SQL DB's host
        :param port: the SQL DB's port
        :param user: the DB's name you want to connect
        :param passwd: the DB's passwd you want to connect
        :param charset: the offset in the DB
        """
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._charset = charset

    @contextlib.asynccontextmanager
    async def __connection(self):
        """
        use the class member to connect to the SQL DB
        you must use it like:
        ### with __connection():
        ###     do something
        it will auto execute the block after yield
        :return:
        """
        self._conn = pymysql.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd,
                                     charset=self._charset)
        self._cursor = self._conn.cursor()
        yield
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    async def query(self, table_name: str) -> str:
        """
        use self.__connection() to connect the SQL
        :param table_name: the table you want to query in the DB
        :return: return a str that correspond your query
        """
        async with self.__connection():
            self._cursor.execute('''use %s''' % config.DB_USER)
            self._cursor.execute("create table if not exists %s (method varchar(100)) " % table_name)
            self._cursor.execute('''select * from %s''' % table_name)
            res = self._cursor.fetchall()
            return '不好意思，暂时没有这个问题的解决方案哦。可以联系管理员进行该词条问题更新。' if len(res) == 0 else res[0][0]

    async def __insert(self, table_name: str, data: str):
        """
        use self.__connection() to connect the SQL
        :param table_name: the table you want to insert in the DB
        :param data: the data you want to insert to the table
        :return:
        """
        async with self.__connection():
            self._cursor.execute('''use %s''' % config.DB_USER)
            self._cursor.execute('''create table if not exists %s (method varchar(100)) ''' % table_name)
            self._cursor.execute('''insert into %s values('%s')''' % (table_name, data))

    async def update(self, table_name: str, data: str):
        """
        use self.__connection() to connect the SQL
        :param table_name: the table you want to update in the DB
        :param data: the data you want to update to the table
        :return:
        """
        async with self.__connection():
            self._cursor.execute('''use %s''' % config.DB_USER)
            self._cursor.execute('''create table if not exists %s (method varchar(100)) ''' % table_name)
            if self._cursor.execute('''select * from %s''' % table_name):
                self._cursor.execute('''update %s set method='%s' ''' % (table_name, data))
                return
        # write after 'with ...:' because __insert() will make a connection to the DB,
        # you must close the update()'s connection first
        await self.__insert(table_name, data)

# in design pattern, this module is stable
