import mysql.connector
from mysql.connector.constants import ClientFlag




class DbConnector:
    def getConfig(self):
        config = {
            'user': 'root',
            'password': 'yD0sP7fqBcwi',
            'host': '34.105.173.105',
            'database': 'data',
            'client_flags': [ClientFlag.SSL],
            'ssl_ca': './certificates/server-ca.pem',
            'ssl_cert': './certificates/client-cert.pem',
            'ssl_key': './certificates/client-key.pem'
        }
        return config

    def getConn(self):
        # now we establish our connection
        config = self.getConfig()
        conn = mysql.connector.connect(**config)
        return conn

    def closeConn(self, conn):
        conn.close
        return
