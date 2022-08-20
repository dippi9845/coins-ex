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
    
    def __random_time(self, sep=":", seed=31415) -> str:
        set_seed(seed)
        d = randint(1, int(time()))
        return datetime.fromtimestamp(d).strftime('%H' + sep + '%M' + sep + '%S')

    def __insert_order(self, ticker_buy : str, ticker_sell : str, amount_buy : int=None, amount_sell : int=None, user_id : int=None, address_in : str=None, address_out : str=None, date : str=None, rnd_time : str=None) -> int:
        
        if amount_buy is None:
            amount_buy = self.__random_int()

        if amount_sell is None:
            amount_sell = self.__random_int()
        
        if user_id is None:
            user_id = self.__random_int()
        
        if address_in is None:
            address_in = sha256(randbytes(20)).hexdigest()

        if address_out is None:
            address_out = sha256(randbytes(20)).hexdigest()
        
        if date is None:
            date = self.__random_date()
        
        if rnd_time is None:
            rnd_time = self.__random_time()

        self.db.insert_into(f"""
        INSERT INTO Ordine
        (UserID, `Ticker compro`, `Ticker vendo`, `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`, Data, Ora)
        VALUES ({user_id}, '{ticker_buy}', '{ticker_sell}', {amount_buy}, {amount_sell}, '{address_in}', '{address_out}', '{date}', '{rnd_time}')
        """)

        return self.db.insered_id()

    def __make_transaction(self, address_in : str, address_out : str, ticker : str, amount : int, wallet : bool) -> int:
        date = datetime.now()
        self.db.insert_into(f'''
            INSERT INTO transazione (`Indirizzo Entrata`, `Indirizzo Uscita`, Ticker, Quantita, Data, Ora)
            VALUES
            ('{address_in}', '{address_out}', '{ticker}', {amount}, '{date.year}-{date.month}-{date.day}', '{date.hour}:{date.minute}:{date.second}')
        ''')

        transaction_id = self.db.insered_id()
        
        if wallet == True:
            table = "wallet"
            
        
        elif wallet == False:
            table = "contocorrente"
       
        self.db.update(f"UPDATE {table} SET Saldo = Saldo - {amount} WHERE Indirizzo='{address_out}'")
        self.db.update(f"UPDATE {table} SET Saldo = Saldo + {amount} WHERE Indirizzo='{address_in}'")

        return transaction_id

    def __complete_order(self, order_id : int, address_sell : str=None, address_buy : str=None):
        # manual tested
        if address_sell is None:
            address_sell = sha256(randbytes(20)).hexdigest()
        
        if address_buy is None:
            address_buy = sha256(randbytes(20)).hexdigest()

        order = self.db.select(f"""
        SELECT `Indirizzo compro`, `Indirizzo vendo`, `Quantita compro`, `Quantita vendo`, `Ticker compro`, `Ticker vendo` FROM Ordine
        WHERE OrdineID={order_id}
        """)[0]
        
        cryptos_ticker = self.db.select("SELECT Ticker FROM crypto")[0]
        
        if order[4] in cryptos_ticker:
            trans_cry = self.__make_transaction(order[0], address_sell, order[4], order[2], wallet=True)
            trans_eur = self.__make_transaction(address_buy, order[1], order[5], order[3], wallet=False)
            
        
        elif order[5] in cryptos_ticker:
            trans_eur = self.__make_transaction(order[0], address_sell, order[4], order[2], wallet=False)
            trans_cry = self.__make_transaction(address_buy, order[1], order[5], order[3], wallet=True)
        
        else:
            raise TypeError("no ticker in crypto")
        
        self.db.insert_into(f"INSERT INTO scambio (`Transazione crypto`, `Transazione fiat`) VALUES ({trans_cry}, {trans_eur})")
        self.db.delete(f"DELETE FROM ordine WHERE OrdineID={order_id}")


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
        cryptos_ticker = self.db.select("SELECT Ticker FROM crypto")[0]
        self.assertIn("BTC", cryptos_ticker)

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
        
        self.db.insert_into(f'''
            INSERT INTO wallet (ATM_ID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({self.__random_int()}, "{sha256(self.__random_string().encode()).hexdigest()}", 0, "{name}", "BTC")
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
            INSERT INTO transazione (`Indirizzo Entrata`, `Indirizzo Uscita`, Ticker, Quantita, Data, Ora)
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

    def test_sell_and_buy(self):
        set_seed(time())

        user1 = self.__random_int()
        user2 = self.__random_int()
        
        btc_addr1 = sha256(randbytes(20)).hexdigest()
        eur_addr1 = sha256(randbytes(20)).hexdigest()

        btc_addr2 = sha256(randbytes(20)).hexdigest()
        eur_addr2 = sha256(randbytes(20)).hexdigest()

        start_amount_btc1 = 2
        start_amount_eur1 = 30000
        start_amount_btc2 = 1
        start_amount_eur2 = 30000
        

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user1}, "{btc_addr1}", {start_amount_btc1}, "{self.__random_string()}", "BTC")
        ''')

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user2}, "{btc_addr2}", {start_amount_btc2}, "{self.__random_string()}", "BTC")
        ''')
        
        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user1}, "{eur_addr1}", {start_amount_eur1}, "{self.__random_string()}", "EUR")
        ''')

        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user2}, "{eur_addr2}", {start_amount_eur2}, "{self.__random_string()}", "EUR")
        ''')
        

        self.__insert_order("EUR", "BTC", amount_buy=20000, amount_sell=1)
        self.__insert_order("EUR", "BTC", amount_buy=19000, amount_sell=1)
        self.__insert_order("EUR", "BTC", amount_buy=18000, amount_sell=1, address_in=eur_addr2, address_out=btc_addr2)
        self.__insert_order("EUR", "BTC", amount_buy=17000, amount_sell=1)
        self.__insert_order("EUR", "BTC", amount_buy=16000, amount_sell=1)
        self.__insert_order("EUR", "BTC", amount_buy=15000, amount_sell=1)

        # tollerance test
        tollerance = 0.1
        amount_buy = 17501
        orders = self.db.select(f'''
        SELECT `Indirizzo compro`, `Quantita compro`, `Indirizzo vendo` FROM Ordine
        WHERE `Ticker compro`="EUR" AND `Ticker vendo`="BTC" AND
        `Quantita compro` BETWEEN {int(amount_buy * (1-tollerance))} AND {int(amount_buy * (1+tollerance))}
        ''')
        
        sells = list(map(lambda x: x[1], orders))
        
        self.assertIn(19000, sells)
        self.assertIn(18000, sells)
        self.assertIn(17000, sells)
        self.assertIn(16000, sells)
        self.assertNotIn(20000, sells)
        self.assertNotIn(15000, sells)

        # most near test
        orders.sort(key=lambda x: abs(amount_buy - x[1]))
        self.assertEqual(orders[0][1], 18000)
        self.assertEqual(orders[0][0], eur_addr2)
        self.assertEqual(orders[0][2], btc_addr2)

        # voglio euro per btc
        # mando euro a lui
        trans_eur = self.__make_transaction(eur_addr2, eur_addr1, "EUR", orders[0][1], wallet=False)
        final_eur1 = self.db.select(f"SELECT Saldo FROM contocorrente WHERE Indirizzo='{eur_addr1}'")[0][0]
        final_eur2 = self.db.select(f"SELECT Saldo FROM contocorrente WHERE Indirizzo='{eur_addr2}'")[0][0]
        
        self.assertEqual(final_eur1, start_amount_eur1 - orders[0][1])
        self.assertEqual(final_eur2, start_amount_eur2 + orders[0][1])


        # ricevo btc da lui
        trans_cry =self.__make_transaction(btc_addr1, btc_addr2, "BTC", 1, wallet=True)
        final_btc1 = self.db.select(f"SELECT Saldo FROM wallet WHERE Indirizzo='{btc_addr1}'")[0][0]
        final_btc2 = self.db.select(f"SELECT Saldo FROM wallet WHERE Indirizzo='{btc_addr2}'")[0][0]
        
        self.assertEqual(final_btc1, start_amount_btc1 + 1)
        self.assertEqual(final_btc2, start_amount_btc2 - 1)

        self.db.insert_into(f"INSERT INTO scambio (`Transazione crypto`, `Transazione fiat`) VALUES ({trans_cry}, {trans_eur})")
        
        self.db.execute("DELETE FROM Ordine")
        ## inverted
        set_seed(time())
        
        user1 = self.__random_int()
        user2 = self.__random_int()
        
        btc_addr1 = sha256(randbytes(20)).hexdigest()
        eur_addr1 = sha256(randbytes(20)).hexdigest()

        btc_addr2 = sha256(randbytes(20)).hexdigest()
        eur_addr2 = sha256(randbytes(20)).hexdigest()

        start_amount_btc1 = 1500
        start_amount_eur1 = 30000
        start_amount_btc2 = 1500
        start_amount_eur2 = 30000
        

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user1}, "{btc_addr1}", {start_amount_btc1}, "{self.__random_string()}", "BTC")
        ''')

        self.db.insert_into(f'''
            INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user2}, "{btc_addr2}", {start_amount_btc2}, "{self.__random_string()}", "BTC")
        ''')
        
        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user1}, "{eur_addr1}", {start_amount_eur1}, "{self.__random_string()}", "EUR")
        ''')

        self.db.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({user2}, "{eur_addr2}", {start_amount_eur2}, "{self.__random_string()}", "EUR")
        ''')

        self.__insert_order("BTC", "EUR", amount_buy=1100, amount_sell=20000)
        self.__insert_order("BTC", "EUR", amount_buy=1000, amount_sell=19000)
        self.__insert_order("BTC", "EUR", amount_buy=900, amount_sell=18000, address_in=btc_addr2, address_out=eur_addr2)
        self.__insert_order("BTC", "EUR", amount_buy=800, amount_sell=17000)
        self.__insert_order("BTC", "EUR", amount_buy=700, amount_sell=16000)
        self.__insert_order("BTC", "EUR", amount_buy=600, amount_sell=15000)

        # tollerance test
        tollerance = 0.1
        amount_buy = 851
        orders = self.db.select(f'''
        SELECT `Indirizzo compro`, `Quantita compro`, `Indirizzo vendo` FROM Ordine
        WHERE `Ticker compro`="BTC" AND `Ticker vendo`="EUR" AND
        `Quantita compro` BETWEEN {int(amount_buy * (1-tollerance))} AND {int(amount_buy * (1+tollerance))}
        ''')

        sells = list(map(lambda x: x[1], orders))
        self.assertNotIn(1100, sells)
        self.assertNotIn(1000, sells)
        self.assertIn(900, sells)
        self.assertIn(800, sells)
        self.assertNotIn(700, sells)
        self.assertNotIn(600, sells)

        # most near test
        orders.sort(key=lambda x: abs(amount_buy - x[1]))
        self.assertEqual(orders[0][1], 900)
        self.assertEqual(orders[0][0], btc_addr2)
        self.assertEqual(orders[0][2], eur_addr2)

        self.__make_transaction(btc_addr2, btc_addr1, "BTC", orders[0][1], wallet=True)
        final_btc1 = self.db.select(f"SELECT Saldo FROM wallet WHERE Indirizzo='{btc_addr1}'")[0][0]
        final_btc2 = self.db.select(f"SELECT Saldo FROM wallet WHERE Indirizzo='{btc_addr2}'")[0][0]

        self.db.execute("DELETE FROM Ordine")

    def test_medium_price(self):
        self.db.delete("DELETE FROM scambio")
        
        cry = []
        fiat = []
        for _ in range(10):
            c = self.__random_int()
            f = self.__random_int()
            
            cry.append(c)
            fiat.append(f)

            order = self.__insert_order("BTC", "EUR", amount_buy=c, amount_sell=f)
            self.__complete_order(order)
        
        rtr = self.db.select(f"""
            SELECT t1.Quantita as crypto, t2.Quantita as fiat
            FROM scambio s
            LEFT JOIN transazione t1 ON s.`Transazione crypto` = t1.ID
            LEFT JOIN transazione t2 ON s.`Transazione fiat` = t2.ID
            WHERE t1.Ticker="BTC" AND t2.Ticker="EUR";
        """)

        numerator = 0

        for i, j in zip(cry, fiat):
            numerator += i * j

        expected_medium = numerator / sum(fiat)

        numerator = 0

        for i, j in rtr:
            numerator += i * j
        
        actual = numerator/sum(map(lambda x: x[1], rtr))

        self.assertEqual(expected_medium, actual)
        self.db.delete("DELETE FROM scambio")


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