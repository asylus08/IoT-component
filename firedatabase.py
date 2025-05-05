import mysql.connector
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://testiot-7e4d7-default-rtdb.firebaseio.com/'
        })

class Database:

    def __init__(self):
        self.mysql_conn = self.init_mysql_db_connection()

    def init_mysql_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="password",
                database="iot"
            )
            print("[MySQL] Connected successfully.")
            return connection
        except mysql.connector.Error as err:
            print("[MySQL] Connection error:", err)
            return None

    def write_local_data(self, temperature, is_debug):
        if not self.mysql_conn:
            print("[MySQL] No connection.")
            return

        try:
            cursor = self.mysql_conn.cursor()
            cursor.execute('INSERT INTO data (temperature, is_debug) VALUES (%s, %s)', (temperature, is_debug))
            self.mysql_conn.commit()
            print(f'[MySQL] Inserted: temp={temperature}, debug={is_debug}')
            cursor.close()
        except Exception as e:
            print("[MySQL] Write error:", e)

    def write_cloud_data(self, temp, is_debug):
        try:
            ref = db.reference('/data')
            ref.push({
                'temperature': temp,
                'is_debug': is_debug
                #'timestamp': db.ServerValue.TIMESTAMP
            })
            print(f'[Firebase] Data pushed: temp={temp}, debug={is_debug}')
        except Exception as e:
            print("[Firebase] Write error:", e)
