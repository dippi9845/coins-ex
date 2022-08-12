from ex.database import Database, DatabaseConfig
import unittest
import string
from random import choices, randint, sample, seed as set_seed, randbytes
from time import time
from datetime import datetime
from hashlib import sha256

TestConfig = {
    'host' : DatabaseConfig['host'],
    'username' : DatabaseConfig['username'],
    'password' : DatabaseConfig['password'],
    'database_name' : "exchanges_tests"
}

class DatabseTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.db = Database(cofig=TestConfig)
        set_seed(time())

    def __random_code(self) -> str:
        return "".join(sample(choices(string.ascii_letters, k=randint(5, 10)) + choices(string.digits, k=randint(5, 10)), k=10))

    def __random_string(self) -> str:
        set_seed(time())
        return "".join(choices(string.ascii_letters, k=randint(5, 10)))

    def __random_nums(self) -> str:
        return "".join(choices(string.digits, k=randint(5, 10)))
    
    def __random_date(self, sep="-", seed=31415) -> str:
        set_seed(seed)
        d = randint(1, int(time()))
        return datetime.fromtimestamp(d).strftime('%Y' + sep + '%m' + sep + '%d')


    def test_create_user(self):
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
        VALUES('{name}', '{surname}', '{email}', '{password}', '{fiscal_code}', '{nationality}', '{telephone}', '{residence}', '{bith_day}')
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
        self.assertEqual(data[8].strftime('%Y-%m-%d'), str(bith_day), "bith_day is different")

        test_id = self.db.select(f"SELECT ID FROM utente WHERE Email = '{email}' AND Password = '{password}'")[0][0]
        self.assertEqual(user_id, test_id)
    
    def test_create_exchange(self):
        name = self.__random_string()
        sede_operativa = self.__random_string()
        sede_legale = self.__random_string()
        sitoweb = "https://" + self.__random_string()
        nation = self.__random_string()
        fondatore = self.__random_string()

        self.db.insert_into(f'''
        INSERT INTO exchange
        (Nome, `Sede Operativa`, `Sede Legale`, Nazione, `Sito web`, Fondatore)
        VALUES("{name}", "{sede_operativa}", "{sede_legale}", "{nation}", "{sitoweb}", "{fondatore}")
        ''')
        
        user_id = self.db.insered_id()

        data = self.db.select(f'''
        SELECT Nome, `Sede Operativa`, `Sede Legale`, Nazione, `Sito web`, Fondatore
        FROM exchange
        WHERE Nome='{name}'
        ''')
        #self.db.delete(f"DELETE FROM exchange WHERE Nome='{name}'")
        data = data[0]
        self.assertEqual(data[0], name, "name is different")
        self.assertEqual(data[1], sede_operativa, "surname is different")
        self.assertEqual(data[2], sede_legale, "email is different")
        self.assertEqual(data[3], nation, "password is different")
        self.assertEqual(data[4], sitoweb, "fiscal_code is different")
        self.assertEqual(data[5], fondatore, "telephone is different")

    def test_register_to_exchange(self):

        name = self.__random_string()
        sede_operativa = self.__random_string()
        sede_legale = self.__random_string()
        sitoweb = "https://" + self.__random_string()
        nation = self.__random_string()
        fondatore = self.__random_string()

        self.db.insert_into(f'''
        INSERT INTO exchange
        (Nome, `Sede Operativa`, `Sede Legale`, Nazione, `Sito web`, Fondatore)
        VALUES("{name}", "{sede_operativa}", "{sede_legale}", "{nation}", "{sitoweb}", "{fondatore}")
        ''')

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
        VALUES('{name}', '{surname}', '{email}', '{password}', '{fiscal_code}', '{nationality}', '{telephone}', '{residence}', '{bith_day}')
        ''')
        
        user_id = self.db.insered_id()

        #self.db.delete(f"DELETE FROM exchange WHERE Nome='{name}'")
        self.db.insert_into(f"INSERT INTO registrati (ID, Nome) VALUES ({user_id}, '{name}')")

        check_name = self.db.select(f"SELECT Nome FROM registrati WHERE ID = {user_id}")[0][0]
        self.assertEqual(check_name, name)

    def test_is_crypto_ticker(self):
        self.db.insert_into("INSERT INTO crypto VALUES ('Bitcoin', 'BTC')")
        cryptos_ticker = self.db.select("SELECT Ticker FROM crypto")[0]
        self.db.delete("DELETE FROM crypto WHERE Ticker = 'BTC'")
        self.assertTrue("BTC" in cryptos_ticker)

    def test_create_default_wallet(self):
        name = self.__random_string()
        sede_operativa = self.__random_string()
        sede_legale = self.__random_string()
        sitoweb = "https://" + self.__random_string()
        nation = self.__random_string()
        fondatore = self.__random_string()

        self.db.insert_into(f'''
        INSERT INTO exchange
        (Nome, `Sede Operativa`, `Sede Legale`, Nazione, `Sito web`, Fondatore)
        VALUES("{name}", "{sede_operativa}", "{sede_legale}", "{nation}", "{sitoweb}", "{fondatore}")
        ''')

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
        VALUES('{name}', '{surname}', '{email}', '{password}', '{fiscal_code}', '{nationality}', '{telephone}', '{residence}', '{bith_day}')
        ''')

        user_id = self.db.insered_id()

        to_hash = str(user_id).encode() + b"ID" + str(int(time())).encode() + b"RND" + randbytes(10)
        # QUERY create an istance of contocorrente
        
        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{sha256(to_hash).hexdigest()}", 1000, "{name}", "EUR")
        ''')


if __name__ == "__main__":
    from sys import argv
    it = iter(argv)
    next(it)
    cmd = next(it, "tests")
    
    if cmd == "init":
        host = input("Insert hostname (localhost) : ").strip()
        
        if host == "":
            host = "localhost"
        
        user = input("Insert user name (root) -> ")

        if user == "":
            user = "root"

        passw = input(f"Insert {user} password -> ")

        InitConfig = {
            'host' : host,
            'username' : user,
            'password' : passw,
            'database_name' : ''
        }

        executor = Database(cofig=InitConfig)
        with open("test.sql", "r") as f:
            query = f.read().split(";")
        
        for i in query:
            executor.execute(i)
    
    elif cmd == "tests":
        unittest.main()