from calendar import day_abbr
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from packet_trasmitter import PacketTransmitter
from database import Database
from threading import Thread
from json import loads, dumps

class ExchangeCommands(Enum):
    REGISTER = "register"
    GET_COOKIE = "cookie"
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"
    SEND_MONEY = "send"
    BUY = "buy"
    SELL = "sell"
    CREATE_WALLET = "create_wallet"
    FIAT_DEPOSIT = "fiat_deposit"
    ACCOUNT_REPORT = "report"
    COMMAND_SPECIFIER = "cmd"


class ExchangeServer(Thread):

    def __init__(self, exchange_name : str, address : tuple[str, int]=("localhost", 31415), processes : int=1) -> None:
        self.__name = exchange_name
        self.__to_run = True
        self.__address = address
        self.__processes = processes

        self.cmds = {
            ExchangeCommands.REGISTER.value : self._register_user,
            ExchangeCommands.GET_COOKIE.value : self._get_cookie,
            ExchangeCommands.WITHDRAW.value : self._withdraw,
            ExchangeCommands.DEPOSIT.value : self._deposit,
            ExchangeCommands.SEND_MONEY : self._send,
            ExchangeCommands.BUY.value : self._buy,
            ExchangeCommands.SELL.value : self._sell,
            ExchangeCommands.CREATE_WALLET.value : self._create_wallet,
            ExchangeCommands.FIAT_DEPOSIT.value : self._create_account_fiat, 
            ExchangeCommands.ACCOUNT_REPORT.value : self._get_report
        }
    
    def set_address(self, addr : tuple[str, int]):
        self.__address = addr

    def __make_transaction(self):
        '''
        perform a generic transaction
        '''
        pass
    
    def __create_account(self) -> str:
        '''
        create a generic account wallet / account fiat
        '''
        pass

    def __check_cookie(self, cookie : str) -> bool | str:
        # QUERY:
        rtr = self.__database.select(f"SELECT ID FROM utente WHERE Cookie = '{cookie}'")
        
        if len(rtr) == 0:
            return False
        
        else:
            return rtr[0]

    def _register_user(self, d : dict) -> bool:
        '''
        register an new user
        '''
        # name : str, surname : str, email : str, password : str, fiscal_code : str, nationality : str, telephone : str
        # aggiungi utente al database
        # crea un conto in euro
        print("register requested", dumps(d))
        self._get_cookie({"email" : d.get("email"), "password" : d.get("password"), "address": d.get("address")})
        pass
    
    def _get_cookie(self, d : dict) -> None:
        '''
        send back the cookie to the client
        '''
        email = d.get("email")
        password = d.get("password")
        # QUERY
        cookie = self.__database.select(f"SELECT Cookie FROM utente WHERE Email = {email} AND Password = {password}")
        self.__reciver.send_data(cookie[0], d.get("address"))

    def _get_report(self, d : dict):
        '''
        returns the report of the user
        '''
        # restituisci il saldo di tutti conti correnti
        print("get report requested", dumps(d))
        pass

    def _withdraw(self, d : dict):
        '''
        withdraw fiat money 
        '''
        print("withdraw requested", dumps(d))
        pass

    def _deposit(self, d : dict):
        '''
        deposit fiat money
        '''
        print("deposit requested", dumps(d))
        pass

    def _send(self, d : dict):
        '''
        send money to another user
        '''
        print("send requested", dumps(d))
        pass

    def _sell(self, d : dict):
        '''
        sell a crypto
        '''
        # controlla che non ci siano ordini di compra vicini nel database, usa quelli
        # altrimetti piazzane uno
        print("sell requested", dumps(d))
        pass

    def _buy(self, d : dict):
        '''
        buy a crypto
        '''
        # controlla che non ci siano ordini di vendita vicini nel database, usa quelli
        # altrimetti piazzane uno
        print("buy requested", dumps(d))
        pass

    def _create_wallet(self, d : dict) -> str:
        '''
        create a wallet
        '''
        print("wallet creation requested", dumps(d))
        pass

    def _create_account_fiat(self, d : dict) -> str:
        '''
        create an account that contais only fiat money
        '''
        print("fiat account requested", dumps(d))
        pass

    def __wait_for_command(self) -> dict:
        data = None
        addr = None
        
        while data is None and addr is None:
            try:
                data, addr = self.__reciver.get_data(timeout_error="", timeout_end="")
            except OSError:
                pass
        
        d = loads(data)
        d.update({"address" : addr})
        return d

    def _close(self, *arguments):
        self.__database.delete(f"DELETE FROM server WHERE host = '{self.__address[0]}' AND port = {self.__address[1]}")
        self.__reciver.close()
        self.__database.close()
        self.__pool.shutdown(wait=True)
    
    def run(self):
        '''
        run the exchange,
        will handle for user connections 
        '''
        self.__database = Database()
        self.__reciver = PacketTransmitter(bind=True, bind_addr=self.__address)
        self.__pool = ThreadPoolExecutor(max_workers=self.__processes)
        
        self.__database.insert_into(f"INSERT INTO server VALUES ('{self.__name}', '{self.__address[0]}', {self.__address[1]})")
        
        while self.__to_run:
            d = self.__wait_for_command()
            self.__pool.submit(self.cmds.get(d.get(ExchangeCommands.COMMAND_SPECIFIER.value)), d)
        
        self._close()
    
    def stop(self):
        self.__to_run = False
    

if __name__ == "__main__":
    from sys import argv
    iter = iter(argv)
    next(iter)
    
    try:
    
        name = next(iter)
        
        if name == "-h":
            print("[name: (required)]")
            exit(0)

    except StopIteration:
        print("you have to provide a name of the exchange")
        exit(0)
    
    port = next(iter, 31415)
    host = next(iter, "localhost")
    workers = next(iter, 1)
    exc = ExchangeServer(name, (host, port), processes=workers)
    exc.run()
