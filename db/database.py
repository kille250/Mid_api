import sqlite3


class database():
    def __init__(dbname):
        self._con = sqlite3.connect(dbname)

    @property
    def con(self):
        return self._con

    @con.setter
    def con(self, value):
        self._con = value

    @con.deleter
    def con(self):
        del self._con
