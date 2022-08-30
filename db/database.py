from functools import wraps
import sqlite3


def dbconnection(dbname):
    def wrapper(fun):
        @wraps(fun)
        def inner_function(*args, **kwargs):
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            kwargs['cur'] = cur
            fun(*args, **kwargs)
            con.commit()
            con.close()
        return inner_function
    return wrapper


@dbconnection('db/midApi.db')
def createTable(cur):
    query = "create table test(id, name, test)"
    cur.execute(query)
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())


createTable()
