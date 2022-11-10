from typing import Any, Callable
from view import View, TerminalView
from database import Database
from hashlib import sha256
from time import time
from random import randbytes, uniform
from datetime import datetime
from threading import Thread
from time import sleep
from random import choices, randint, sample, seed as set_seed, randbytes
import string
from sys import argv
import signal
from math import sin, cos

active_fake_users = []


def stop_fake_users(signal, fname):
    for index, user in enumerate(active_fake_users):
        user.stop()
        user.join()
        print(f"Stopped fake user {index}")


class User:

    def __init__(self, view : View) -> None:
        self.__view = view
        
        self.access_exchange = {
            "register" : self._register,
            "access" : self._access
        }

        self.exchange_commands = {
            "deposit" : self._deposit,
            "withdraw" : self._withdraw,
            "sell" : self._sell,
            "buy" : self._buy,
            "report" : self._report,
            "exit" : self.exit
        }
        
        self.__exchange_name = None
        self.__access_info = None
        self.__registered_exchanges = []
        self.__database = Database()

    def __make_transaction(self, address_in : str, address_out : str, ticker : str, amount : int, wallet : bool) -> Any:
        date = datetime.now()
        # QUERY create a transaction
        # TESTED
        self.__database.insert_into(f'''
            INSERT INTO transazione (`Indirizzo Entrata`, `Indirizzo Uscita`, Ticker, Quantita, Data, Ora)
            VALUES
            ('{address_in}', '{address_out}', '{ticker}', {amount}, '{date.year}-{date.month}-{date.day}', '{date.hour}:{date.minute}:{date.second}')
        ''')

        transaction_id = self.__database.insered_id()
        
        if wallet == True:
            table = "wallet_utente"
        
        elif wallet == False:
            table = "contocorrente"
       
        # QUERY
        # TESTED
        self.__database.update(f"UPDATE {table} SET Saldo = Saldo - {amount} WHERE Indirizzo='{address_out}'")
        # QUERY
        # TESTED
        self.__database.update(f"UPDATE {table} SET Saldo = Saldo + {amount} WHERE Indirizzo='{address_in}'")

        return transaction_id

    def __is_crypto_ticker(self, ticker : str) -> bool:
        # QUERY
        # TESTED
        cryptos_ticker = self.__database.select("SELECT Ticker FROM crypto")
        return ticker in cryptos_ticker

    def _first_access(self):
        
        name = self.__view.ask_input("Insert Name -> ")
        surname = self.__view.ask_input("Insert Surname -> ")
        email = self.__view.ask_input("Insert Emai -> ")
        password = self.__view.ask_input("Insert Password -> ")
        fiscal_code = self.__view.ask_input("Insert Fiscal Code -> ")
        nationality = self.__view.ask_input("Insert Natinality -> ")
        telephone = self.__view.ask_input("Insert Telephone -> ")
        residence = self.__view.ask_input("Insert Residence -> ")
        bith_day = self.__view.ask_input("Insert Bith Day -> ")

        to_register = self.__view.menu("Choose the first exchange", self._current_exchanges())

        # QUERY insert utente instance
        # TESTED
        self.__database.insert_into(f'''
        INSERT INTO utente
        (Nome, Cognome, Email, Password, `Codice Fiscale`, Nazionalita, `Numero Di Telefono`, Residenza, `Data di nascita`)
        VALUES('{name}', '{surname}', '{email}', '{password}', '{fiscal_code}', '{nationality}', '{telephone}', '{residence}', '{bith_day}')
        ''')

        self.__access_info = self.__database.insered_id()

        self._register(to_register)
        
    def _register(self, exchange_name : str):
        '''
        register the user to the exchange provided as paramenter
        '''
        if self.__access_info is not None:
            # QUERY register to that exchange
            # TESTED
            self.__database.insert_into(f"INSERT INTO registrati (ID, Nome) VALUES ({self.__access_info}, '{exchange_name}')")
            self._create_fiat_account(exchange_name)
            self.__registered_exchanges.append(exchange_name)

    def _set_exchange(self, name : str):
        self.__exchange_name = name

    def _current_exchanges(self) -> list[str]:
        '''
        list all currrent databases
        '''
        # QUERY get all existing exchanges
        # TESTED
        rtr = self.__database.select("SELECT Nome FROM exchange")
        rtr = list(map(lambda x: x[0], rtr))
        return rtr

    def _access(self) -> bool:
        '''
        Asks only the credentials
        '''
        
        email = self.__view.ask_input("insert email -> ")
        password = self.__view.ask_input("insert password -> ")
        
        # QUERY get id
        # TESTED
        resp = self.__database.select(f"SELECT ID FROM utente WHERE Email = '{email}' AND Password = '{password}'")
        
        if len(resp) == 0:
            return False

        user_id = resp[0]
        self.__access_info = user_id
        # QUERY get registerd exchnges
        # TESTED
        resp = self.__database.select(f"SELCECT Nome FROM registrati WHERE ID = {user_id}")
        self.__registered_exchanges = list(map(lambda x: x[0], resp))
        return True

    def _create_wallet(self, exchange_name : str, crypto_ticker : str):
        if self.__access_info is not None:
            to_hash = str(self.__access_info).encode() + b"ID" + str(int(time())).encode() + b"RND" + randbytes(10)
            # QUERY create an istance of contocorrente
            
            self.__database.insert_into(f'''
                INSERT INTO wallet (UserID, Indirizzo, Saldo, Nome, Ticker)
                VALUES ({self.__access_info}, "{sha256(to_hash).hexdigest()}", 0, "{exchange_name}", "{crypto_ticker}")
            ''')

    def _create_fiat_account(self, exchange_name : str, fiat_ticker : str="EUR", amount : int=1000):
        if self.__access_info is not None:
            to_hash = str(self.__access_info).encode() + b"ID" + str(int(time())).encode() + b"RND" + randbytes(10)
            
            # QUERY create an istance of contocorrente
            # TESTED
            self.__database.insert_into(f'''
                INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
                VALUES ({self.__access_info}, "{sha256(to_hash).hexdigest()}", {amount}, "{exchange_name}", "{fiat_ticker}")
            ''')
    
    def _report(self):
        '''
        request a report from the exchange
        '''
        # QUERY gets all wallets
        # TESTED
        wallets = self.__database.select(f"SELECT Indirizzo, Saldo, Ticker FROM wallet_utente WHERE UserID={self.__access_info}")
        self.__view.show_message("Wallets:")

        for wallet in wallets:
            self.__view.show_message(f"Address: {wallet[0]}, contains: {wallet[1]}, balance: {wallet[2]}")

        # QUERY gets all fiat accounts
        # TESTED
        accounts = self.__database.select(f"SELECT Indirizzo, Saldo, Ticker FROM contocorrente WHERE UserID={self.__access_info}")
        self.__view.show_message("Accounts:")
        
        for account in accounts:
            self.__view.show_message(f"Address: {account[0]}, contains: {account[1]}, balance: {account[2]}")
    
    def _sell(self, address_buy : str, address_sell : str, ticker_sell : str, ticker_buy : str, amount_sell : int, amount_buy : int, tollerance : float=0.1):
        '''
        want to sell crypto
        '''
        # QUERY get all order of buy for this crypto and the amount in the other currency
        buys = self.__database.select(f'''
        SELECT OrdineID, `Quantita compro` FROM Ordine
        WHERE `Ticker compro`="{ticker_sell}" AND `Ticker vendo`="{ticker_buy}" AND
        `Quantita compro` BETWEEN {amount_buy * (1-tollerance)} AND {amount_buy * (1+tollerance)}
        ''')

        if len(buys) > 0:
            buys = list(buys)
            # sort all buys from the most near one to the most far one
            buys.sort(key=lambda x: abs(amount_buy - x[1]))
            best_order_id = buys[0][0]

            # QUERY get order target info
            order_data = self.__database.select(f'''
                SELECT `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`
                FROM transazione
                WHERE OrdineID = {best_order_id}
            ''')
            order_data = order_data[0]

            to_send_addr = order_data[2]

            # transaction to one who want to buy this coin
            id1 = self.__make_transaction(to_send_addr, address_sell, ticker_sell, amount_sell)
            
            to_recive_addr = order_data[3]
            amount_buy = order_data[0]

            # transaction to me
            id2 = self.__make_transaction(address_buy, to_recive_addr, ticker_buy, amount_buy)

            # QUERY delete the order
            self.__database.delete(f"DELETE FROM ordine WHERE OrdineID = {best_order_id}")

            if self.__is_crypto_ticker(ticker_sell):
                crypto_transaction = id1
                fiat_transaction = id2
            else:
                crypto_transaction = id2
                fiat_transaction = id1

            # QUERY put into scambio table
            self.__database.insert_into(f'''
                INSERT INTO scambio (`Transazione crypto`, `Transazione fiat`)
                VALUES ({crypto_transaction}, {fiat_transaction})
            ''')


        else:
            # place an order and wait to be compleated
            date = datetime.now()
            
            # QUERY for inser an order
            self.__database.insert_into(f'''
                INSERT INTO Ordine (UserID, `Ticker compro`, `Ticker vendo`, `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`, Data, Ora)
                VALUES ({self.__access_info}, "{ticker_buy}", "{ticker_sell}", "{amount_buy}", "{amount_sell}", "{address_buy}", "{address_sell}", "{date.year}-{date.month}-{date.day}", "{date.hour}:{date.minute}:{date}")
            ''')

    def _buy(self, address_buy : str, address_sell : str, ticker_sell : str, ticker_buy : str, amount_sell : int, amount_buy : int, tollerance : float=0.1):
        '''
        want to buy crypto
        '''
        # QUERY get all order of sell for this crypto and the amount in the other currency
        sells = self.__database.select(f'''
        SELECT OrdineID, `Quantita compro` FROM Ordine
        WHERE `Ticker compro`="{ticker_sell}" AND `Ticker vendo`="{ticker_buy} AND
        `Quantita compro` BETWEEN {amount_buy * (1-tollerance)} AND {amount_buy * (1+tollerance)}
        ''')

        if len(sells) > 0:
            sells = list(sells)
            # sort all buys from the most near one to the most far one
            sells.sort(key=lambda x: abs(amount_buy - x[1]))
            best_order_id = sells[0][0]

            # QUERY get order target info
            order_data = self.__database.select(f'''
                SELECT `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`
                FROM transazione
                WHERE OrdineID = {best_order_id}
            ''')
            order_data = order_data[0]

            to_send_addr = order_data[2]

            # transaction to one who want to sell this coin
            id1 = self.__make_transaction(to_send_addr, address_sell, ticker_sell, amount_sell)
            
            to_recive_addr = order_data[3]
            amount_buy = order_data[0]

            # transaction to me
            id2 = self.__make_transaction(address_buy, to_recive_addr, ticker_buy, amount_buy)

            # QUERY delete the order
            self.__database.delete(f"DELETE FROM ordine WHERE OrdineID = {best_order_id}")

            if self.__is_crypto_ticker(ticker_sell):
                crypto_transaction = id1
                fiat_transaction = id2
            else:
                crypto_transaction = id2
                fiat_transaction = id1

            # QUERY put into scambio table
            self.__database.insert_into(f'''
                INSERT INTO scambio (`Transazione crypto`, `Transazione fiat`)
                VALUES ({crypto_transaction}, {fiat_transaction})
            ''')


        else:
            # place an order and wait to be compleated
            date = datetime.now()
            
            # QUERY for inser an order
            self.__database.insert_into(f'''
                INSERT INTO Ordine (UserID, `Ticker compro`, `Ticker vendo`, `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`, Data, Ora)
                VALUES ({self.__access_info}, "{ticker_buy}", "{ticker_sell}", "{amount_buy}", "{amount_sell}", "{address_buy}", "{address_sell}", "{date.year}-{date.month}-{date.day}", "{date.hour}:{date.minute}:{date}")
            ''')

    def _withdraw(self, atm_id : str, crypto_ticker : str, fiat_ticker : str, amount_fiat : int, user_addr : str):
        '''
        withdraw fiat money 
        '''
        now = datetime.now()
        spread = self.__database.select(f"SELECT spread FROM atm WHERE `Codice Icentificativo`='{atm_id}'")[0]
        countervalue = self.__database.get_countervalue_by_time(fiat_ticker, crypto_ticker, f"{now.year}-{now.month}-{now.day}", "00:00:00", f"{now.hour}:{now.minute}:{now.second}")
        excahnge_price = countervalue - spread
        crypto_amount = amount_fiat/excahnge_price

        atm_addr = self.__database.select(f"SELECT Indirizzo FROM wallet_atm WHERE ATM_ID='{atm_id}' AND Ticker='{crypto_ticker}'")[0]
        
        date = datetime.now()
        
        # QUERY create a transaction
        # TESTED
        self.__database.insert_into(f'''
            INSERT INTO transazione (`Indirizzo Entrata`, `Indirizzo Uscita`, Ticker, Quantita, Data, Ora)
            VALUES
            ('{atm_addr}', '{user_addr}', '{user_addr}', {user_addr}, '{date.year}-{date.month}-{date.day}', '{date.hour}:{date.minute}:{date.second}')
        ''')
        
        # QUERY
        # TESTED
        self.__database.update(f"UPDATE wallet_utente SET Saldo = Saldo - {crypto_amount} WHERE Indirizzo='{user_addr}'")
        # QUERY
        # TESTED
        self.__database.update(f"UPDATE wallet_atm SET Saldo = Saldo + {crypto_amount} WHERE Indirizzo='{atm_addr}'")

        # decrease the amount of fiat money in the atm
        
        

    def _deposit(self):
        '''
        deposit fiat money
        '''
        pass

    def run(self):
        '''
        keep intercting with the user
        '''
        while True:
            excs = self._current_exchanges()
            possibles = set(excs)
            possibles.update({"", "update"})

            ch = self.__view.menu("Choose avaiable exchanges", possibles)
            
            if ch == "":
                break

            elif ch == "update":
                continue

            self._set_exchange(ch)

            ch = self.__view.menu(f"Do you want to register or access to {self.__exchange_name}", ["register", "access"])
            
            if self.access_exchange[ch]():
                while ch != "exit":
                    ch = self.__view.menu(f"What do you want to do on {self.__exchange_name} ?", self.exchange_commands.keys())
                    self.exchange_commands[ch]()
            else:
                print(f"error during {ch}")


    def exit(self):
        '''
        exit from the current exchange
        '''
        self.__access_info = None
        self.__database.close()
    

def fluttuation_price(time: int) -> float:
    '''
        this function returns the price of the crypto
        at the time passed as parameter
    '''
    return 0.015 * time + sin(2 * time) + cos(3 * time) + 3

def noise(price: float) -> float:
    '''
        this function adds a random noise to the price
    '''
    return price + uniform(-0.015 * price, 0.015 * price)


class FakeUser(Thread):
    
    BUY_STATE = "Buy"
    WAIT_BUY_STATE = "Wait buy"
    SELL_STATE = "Sell"
    WAIT_SELL_STATE = "Wait sell"
    
    
    def __random_string(self) -> str:
        set_seed(time())
        return "".join(choices(string.ascii_letters, k=randint(5, 10)))

    
    def __random_date(self, sep="-", seed=31415) -> str:
        set_seed(seed)
        d = randint(1, int(time()))
        return datetime.fromtimestamp(d).strftime('%Y' + sep + '%m' + sep + '%d')
    
    
    def __random_code(self) -> str:
        return "".join(sample(choices(string.ascii_letters, k=randint(5, 10)) + choices(string.digits, k=randint(5, 10)), k=10))
    
    
    def __random_nums(self) -> str:
        return "".join(choices(string.digits, k=randint(5, 9)))

    
    def __init__(self, initail_state : str, start_time : int = int(time()), fluttuation_price : Callable = fluttuation_price, noise : Callable = noise,  fiat_ticker : str="EUR", crypto_ticker : str="BTC", inital_crypto : int=0, initial_amount : int=1000000, reload_amount : int=1000, polling_rate :float=0.001) -> None:
        super().__init__()
        self.fluttuation_price = fluttuation_price
        self.noise = noise
        self.state = initail_state
        self.start_time = start_time
        
        self.reload_amount = reload_amount # spero di non dover usare sta cosa (quantità di soldi che viene ricaricata ogni volta che finiscono)
        self.initial_amount = initial_amount
        self.inital_crypto = inital_crypto
        self.crypto_ticker = crypto_ticker
        self.fiat_ticker = fiat_ticker
        self.polling_rate = polling_rate
        
        self.is_running = True
        
        self.states = {
            self.BUY_STATE : self.place_buy,
            self.WAIT_BUY_STATE : self.wait_buy,
            self.WAIT_SELL_STATE : self.wait_sell,
            self.SELL_STATE : self.place_sell
        }
        
        self.__database = Database()
        
        name = self.__random_string()
        surname = self.__random_string()
        email = self.__random_string()
        password = self.__random_code()
        fiscal_code = self.__random_code()
        nationality = self.__random_string()
        telephone = self.__random_nums()
        residence = self.__random_string()
        bith_day = self.__random_date()
        
        self.__database.insert_into(f'''
        INSERT INTO utente
        (Nome, Cognome, Email, Password, `Codice Fiscale`, Nazionalita, `Numero Di Telefono`, Residenza, `Data di nascita`)
        VALUES('{name}', '{surname}', '{email}', '{password}', '{fiscal_code}', '{nationality}', '{telephone}', '{residence}', '{bith_day}')
        ''')
        
        self.my_id = self.__database.insered_id()
        
        # nome dell'exchange ceh dovrà essere fornito
        
        self.fiat_address = sha256(str(self.my_id).encode() + b"ID" + str(int(time())).encode() + b"RND" + randbytes(10)).hexdigest()
        self.crypto_address = sha256(str(self.my_id).encode() + b"IfdsgD" + str(int(time())).encode() + b"RNfdsgsdD" + randbytes(10)).hexdigest()
        
        self.__database.insert_into(f'''
            INSERT INTO wallet_utente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({self.my_id}, "{self.crypto_address}", 0, "Exchange name", "{crypto_ticker}")
        ''')
        
        self.__database.insert_into(f'''
            INSERT INTO contocorrente (UserID, Indirizzo, Saldo, Nome, Ticker)
            VALUES ({self.my_id}, "{self.fiat_address}", {self.initial_amount}, "Exchange name", "{fiat_ticker}")
        ''')

    
    def place_buy(self) -> None:
        '''
            this function place a buy order of a crptocurrency
            so the order yields fiat money for cryptocurrency
        '''
        
        price = self.noise(self.fluttuation_price(int(time()) - self.start_time)) # price of 1 crypto
        amount_buy = randint(1, 3) # amount of crypto to buy
        amount_sell = amount_buy * price # amount of fiat money to spend
        
        # TODO CERCARE PRIMA DI INSERIRE
        
        # metti ordine nel database
        # QUERY
        self.__database.insert_into(f'''
        INSERT INTO Ordine
        (UserID, `Ticker compro`, `Ticker vendo`, `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`)
        VALUES ({self.my_id}, '{self.crypto_ticker}', '{self.fiat_ticker}', {amount_buy}, {amount_sell}, '{self.crypto_address}', '{self.fiat_address}')                 
        ''')
        
        self.order_id = self.__database.insered_id()
        self.state = self.WAIT_BUY_STATE
    
    
    def wait_buy(self) -> None:
        
        while len(self.__database.select(f'SELECT * FROM ordine WHERE OrdineID={self.order_id}')) > 0 and self.is_running:
            
            sleep(self.polling_rate)
        
        self.state = self.SELL_STATE
    
    
    def wait_sell(self) -> None:
        
        while len(self.__database.select(f'SELECT * FROM ordine WHERE OrdineID={self.order_id}')) > 0 and self.is_running:
            
            sleep(self.polling_rate)
        
        self.state = self.BUY_STATE
    
    
    def place_sell(self) -> None:
        price = self.noise(self.fluttuation_price(int(time()) - self.start_time))
        
        amount_sell = randint(1, 3) # amount of crypto to buy
        amount_buy = amount_sell * price # amount of fiat money to spend
        
        # TODO CERCARE PRIMA DI INSERIRE
        
        # metti ordine nel database
        # QUERY
        self.__database.insert_into(f'''
        INSERT INTO Ordine
        (UserID, `Ticker compro`, `Ticker vendo`, `Quantita compro`, `Quantita vendo`, `Indirizzo compro`, `Indirizzo vendo`)
        VALUES ({self.my_id}, '{self.fiat_ticker}', '{self.crypto_ticker}', {amount_buy}, {amount_sell}, '{self.fiat_address}', '{self.crypto_address}')                 
        ''')
        
        self.order_id = self.__database.insered_id()
        self.state = self.WAIT_SELL_STATE
    
    
    def stop(self) -> None:
        self.is_running = False
    
    
    def run(self):
        while self.is_running:
            self.states[self.state]()
    
    
    def join(self) -> None:
        return super().join()




if __name__ == "__main__":
    arg_it = iter(argv)
    next(arg_it)
    fake_user_num = int(next(arg_it, 100))
    end = int(fake_user_num/2)
    
    for i in range(end):
        t = FakeUser(FakeUser.BUY_STATE)
        active_fake_users.append(t)
        t.start()
    
    for i in range(end):
        t = FakeUser(FakeUser.SELL_STATE)
        active_fake_users.append(t)
        t.start()
    
    signal.signal(signal.SIGINT, stop_fake_users)
    
    user = User(TerminalView())
    user.run()
    user.exit()
    stop_fake_users(None, None)