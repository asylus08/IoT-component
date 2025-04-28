import mysql.connector

class Database:
    
    def __init__(self):
        self.mysql_conn = self.init_mysql_db_connection()
        self.firebase_conn = self.init_firebase_db_connection()
        
        
    def init_mysql_db_connection(self):
        
        connection = mysql.connector.connect(
            host = "localhost",
            port = 3306,
            user = "root",
            password = "password",
            database = "iot"
        )
        return connection
    
    
    def init_firebase_db_connection(self):
        pass
    
    
    def write_data(self, temp, is_debug):
        cursor = self.mysql_conn.cursor()
        cursor.execute('INSERT INTO data (temp, debug) VALUES (%s, %s)', (temp, is_debug))
        print(f'Result: {cursor.rowcount}')
        cursor.execute('SELECT * FROM data')
        print(cursor.fetchall())
        self.mysql_conn.commit()
        cursor.close()
              

db = Database()

db.write_data(25.6, False)
              
              
        
        