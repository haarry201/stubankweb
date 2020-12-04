import mysql.connector


class DbConnector:
    def getConn(self):
        cnx = mysql.connector.connect(user='root', password='yD0sP7fqBcwi',
                                      host='34.105.173.105',
                                      database='data')
        cnx.close()
