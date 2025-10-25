import mysql.connector,pymysql
from pymysql._auth import caching_sha2_password_auth

from pymysql.cursors import DictCursor
from PyQt5.QtWidgets import QMessageBox as msg
class DatabaseManager:
    def __init__(self,username,password,ip_address,parent):
        self.username =  username
        self.password = password
        self.ip_address = ip_address
        self.parent = parent
    def connect(self):
        try:
            connection = pymysql.connect(
                host = self.ip_address,
                user= self.username,    
                password= self.password,
                database='pupil',
                cursorclass=DictCursor
                
            )
            return connection
        except mysql.connector.Error as e:
            msg.critical(self.parent,'Error', f"Database connection error: {str(e)}")
            return None
    def fetch_details(self,query):
        try:
            data = self.connect()
            cursor = data.cursor()
            if data:
                cursor.execute(query)
                return cursor.fetchall()
            else:
                msg.showerror("Error database is not connected")
        except Exception as e:
            print(e)
    def search_detail(self,query):
        try:
            data = self.connect()
            cursor = data.cursor()
            if data:
                cursor.execute(query)
                return cursor.fetchone()
            else:
                msg.showerror("Error database is not connected")
        except Exception as e:
            print(e)
    def store_data(self,query,values):
       
            data = self.connect()
            cursor = data.cursor()
            if data:
                cursor.execute(query,values)
                data.commit()
            else:
                msg.showerror("Error database is not connected")
        # except Exception as e:
        #     print(e)
    def execute_query(self,query):
            data = self.connect()
            if data:
                cursor = data.cursor()
                cursor.execute(query)
                data.commit()
        
    def delete_data(self,query):
        try:
            data = self.connect()
            if data:
                cursor = data.cursor()
                cursor.execute(query)
                data.commit()
        except Exception:
            pass
    def getDetails(self):
        data = self.connect()
        if data:
            return self.password

