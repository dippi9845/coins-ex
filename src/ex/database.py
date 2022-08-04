import mysql.connector
from json import loads

class Database:
    def __init__(self) -> None:
        
        with open("database_config.json", "r") as f:
            data = loads(f.read())
        
        self.__cnx = mysql.connector.connect(
            host=data['host'],
            user=data['username'],
            password=data['password'],
            database=data["database_name"]
        )

        self.__cursor = self.__cnx.cursor()
    
