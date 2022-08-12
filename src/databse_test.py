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
        return "".join(choices(string.digits, k=randint(5, 9)))
    
    def __random_int(self) -> int:
        return randint(1, 9E8)
    
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

    def test_create_default_contocorrente_and_wallet(self):
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

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{sha256(to_hash).hexdigest()}", 0, "{name}", "BTC")
        ''')

    def test_make_transaction(self):
        set_seed(time())
        addr1 = sha256(randbytes(20)).hexdigest()
        user_id = self.__random_nums()
        name = self.__random_string()

        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr1}", 1000, "{name}", "EUR")
        ''')

        addr2 = sha256(randbytes(20)).hexdigest()
        user_id = self.__random_nums()
        name = self.__random_string()

        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr2}", 1000, "{name}", "EUR")
        ''')

        date = datetime.now()
        # QUERY create a transaction
        self.db.insert_into(f'''
            INSERT INTO transazione (`Indirizzo Entrata`, `Indirizzo Uscita`, Ticker, Quantita, Ora, Data)
            VALUES
            ('{addr1}', '{addr2}', 'EUR', 950, '{date.year}-{date.month}-{date.day}', '{date.hour}:{date.minute}:{date.second}')
        ''')

        self.db.update(f"UPDATE contocorrente SET Saldo = Saldo - 950 WHERE Indirizzo='{addr2}'")
        self.db.update(f"UPDATE contocorrente SET Saldo = Saldo + 950 WHERE Indirizzo='{addr1}'")
        balance1 = self.db.select(f"SELECT Saldo FROM contocorrente WHERE Indirizzo='{addr1}'")[0][0]
        balance2 = self.db.select(f"SELECT Saldo FROM contocorrente WHERE Indirizzo='{addr2}'")[0][0]
        
        self.assertEqual(balance1, 1950, "balance is wrong")
        self.assertEqual(balance2, 50, "balance is wrong")

    def test_report(self):
        set_seed(time())
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

        # exchange name
        name = self.__random_string()

        balance1 = int(self.__random_nums())
        balance2 = int(self.__random_nums())
        balance3 = int(self.__random_nums())
        balance4 = int(self.__random_nums())
        
        addr1 = sha256(randbytes(20)).hexdigest()
        addr2 = sha256(randbytes(20)).hexdigest()
        addr3 = sha256(randbytes(20)).hexdigest()
        addr4 = sha256(randbytes(20)).hexdigest()


        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr1}", {balance1}, "{name}", "BTC")
        ''')

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr2}", {balance2}, "{name}", "BTC")
        ''')

        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr3}", {balance3}, "{name}", "EUR")
        ''')

        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr4}", {balance4}, "{name}", "EUR")
        ''')

        wallets = self.db.select(f"SELECT Indirizzo, Saldo, Ticker FROM wallet WHERE UserID={user_id}")
        self.assertTrue(wallets[0][0] == addr1 or wallets[0][0] == addr2, "wrong address")
        self.assertTrue(wallets[0][1] == balance1 or wallets[0][1] == balance2, "wrong balance")
        self.assertEqual(wallets[0][2], "BTC", "wrong ticker")
        self.assertTrue(wallets[1][0] == addr2 or wallets[1][0] == addr1, "wrong address")
        self.assertTrue(wallets[1][1] == balance2 or wallets[1][1] == balance1, "wrong balance")
        self.assertEqual(wallets[1][2], "BTC", "wrong ticker")

        accounts = self.db.select(f"SELECT Indirizzo, Saldo, Ticker FROM contocorrente WHERE UserID={user_id}")
        self.assertTrue(accounts[0][0] == addr3 or accounts[0][0] == addr4, "wrong address")
        self.assertTrue(accounts[0][1] == balance3 or accounts[0][1] == balance4, "wrong balance")
        self.assertEqual(accounts[0][2], "EUR", "wrong ticker")
        self.assertTrue(accounts[1][0] == addr4 or accounts[1][0] == addr3, "wrong address")
        self.assertTrue(accounts[1][1] == balance4 or accounts[1][1] == balance3, "wrong balance")
        self.assertEqual(accounts[1][2], "EUR", "wrong ticker")

    def test_buy(self):
        pass
    
    def test_sell(self):
        set_seed(time())

        user_id = int(self.__random_nums())

        name = self.__random_string()
        addr1_1 = sha256(randbytes(20)).hexdigest()

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user_id}, "{addr1_1}", 10, "{name}", "BTC")
        ''')

        addr1_1 = sha256(randbytes(20)).hexdigest()

        date = datetime.now()
        
        # test the tollerance
        self.db.insert_into(f"""
        INSERT INTO Ordine
        (UserID, `Ticker compro`, `Ticker vendo`, `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`, Data, Ora)
        VALUES ('BTC', 'EUR', '20000', '1', '{date.year}-{date.month}-{date.day}', '{date.hour}:{date.minute}:{date.second}')
        
        """)
        

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