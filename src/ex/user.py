from typing import Any
from view import View, TerminalView
from database import Database
from hashlib import sha256
from time import time
from random import randbytes
from datetime import datetime

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

    def __make_transaction(self, address_in : str, address_out : str, ticker : str, amount : int) -> Any:
        date = datetime.now()
        # QUERY create a transaction
        self.__database.insert_into(f'''
            INSERT INTO transazione (`Indirizzo Entrata`, `Indirizzo Uscita`, Ticker, Quantita, Ora, Data)
            VALUES
            ('{address_in}', '{address_out}', '{ticker}', {amount}, '{date.year}-{date.month}-{date.day}', '{date.hour}:{date.minute}:{date.second}')
        ''')

        return self.__database.insered_id()

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
        wallets = self.__database.select(f"SELECT Indirizzo, Saldo, Ticker FROM wallet WHERE UserID={self.__access_info}")
        self.__view.show_message("Wallets:")

        for wallet in wallets:
            self.__view.show_message(f"Address: {wallet[0]}, contains: {wallet[1]}, balance: {wallet[2]}")

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
        WHERE `Ticker compro`="{ticker_sell}" AND `Ticker vendo`="{ticker_buy} AND
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

    def _withdraw(self, atm_id : str):
        '''
        withdraw fiat money 
        '''
        pass

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

if __name__ == "__main__":
    user = User(TerminalView())
    user.run()