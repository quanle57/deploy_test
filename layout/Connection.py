import mysql.connector

database1 = {
    "host": 'localhost',
    "user": "root",
    "password": "root",
    "db": 'baemin_revenue',
}
database = {
    "host": 'ls-4b45821b03b4a608b32200f768ffbe9b8e0935d1.cpkjfygl2loj.ap-northeast-2.rds.amazonaws.com',
    "user": "dbmasteruser",
    "password": "87654321",
    "db": 'baemin_revenue',
}


# class user
class ConnectionDB:
    """
    class connect database
    """
    def __init__(self):
        self.host = database['host']
        self.user = database['user']
        self.password = database['password']
        self.name_database = database['db']
        self.connection = None
        self.cursor = None

    def openConnect(self):
        self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                                  database=self.name_database)
        self.cursor = self.connection.cursor(dictionary=True)

    def loadRecord(self, sql): #######
        self.cursor.execute(sql)
        record = self.cursor.fetchone()
        return record

    def loadRecords(self, sql): 
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        return records

    def insertRecord(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def updateRecord(self, sql):  ######
        self.cursor.execute(sql)
        self.connection.commit()

    def deleteRecord(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def closeConnect(self):
        self.connection.close()
        self.cursor.close()
