from ex.database import Database, DatabaseConfig
import unittest
import string
from random import choices, randint, sample

TestConfig = {
    'host' : DatabaseConfig['host'],
    'username' : DatabaseConfig['username'],
    'password' : DatabaseConfig['password'],
    'database_name' : "exchanges_tests"
}

class DatabseTest(unittest.TestCase):

    db = Database(cofig=TestConfig)

    def __random_code(self) -> str:
        return "".join(sample(choices(string.ascii_letters, k=randint(5, 10)) + choices(string.digits, k=randint(5, 10))))

    def __random_string(self) -> str:
        return "".join(choices(string.ascii_letters, k=randint(5, 10)))

    def __random_nums(self) -> str:
        return "".join(choices(string.digits, k=randint(5, 10)))
    
    def __random_date(self, sep="-") -> str:
        return "".join(choices(string.digits, k=4)) + "-" + "".join(choices(string.digits, k=2)) + "-" + "".join(choices(string.digits, k=2))

    def create_user(self):
        name = self.__random_string()
        surname = self.__random_string()
        email = self.__random_string()
        password = self.__random_code()
        fiscal_code = self.__random_code()
        nationality = self.__random_string()
        telephone = self.__random_nums()
        residence = self.__random_string()
        bith_day = self.__random_date()

        self.db.insert_into(f'''
        INSERT INTO utente
        (Nome, Cognome, Email, Password, `Codice Fiscale`, Nazionalita, `Numero Di Telefono`, Residenza, `Data di nascita`)
        VALUES({name}, {surname}, {email}, {password}, {fiscal_code}, {nationality}, {telephone}, {residence}, {bith_day})
        ''')
        
        user_id = self.db.insered_id()

        data = self.db.select(f'''
        SELECT Nome, Cognome, Email, Password, `Codice Fiscale`, Nazionalita, `Numero Di Telefono`, Residenza, `Data di nascita`
        FROM utente
        WHERE ID={user_id}
        ''')
        data = data[0]
        self.assertEqual(data[0], name, "name is different")
        self.assertEqual(data[1], surname, "surname is different")
        self.assertEqual(data[2], email, "email is different")
        self.assertEqual(data[3], password, "password is different")
        self.assertEqual(data[4], fiscal_code, "fiscal_code is different")
        self.assertEqual(data[5], nationality, "nationality is different")
        self.assertEqual(data[6], telephone, "telephone is different")
        self.assertEqual(data[7], residence, "residence is different")
        self.assertEqual(data[8], bith_day, "bith_day is different")



if __name__ == "__main__":

    InitConfig = {
        'host' : DatabaseConfig['host'],
        'username' : DatabaseConfig['username'],
        'password' : DatabaseConfig['password'],
        'database_name' : ''
    }

    executor = Database(cofig=InitConfig)
    with open("test.sql", "r") as f:
        query = f.read().split(";")
    
    for i in query:
        executor.execute(i)
    
    unittest.main()