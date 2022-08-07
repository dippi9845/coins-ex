from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from packet_trasmitter import PacketTransmitter
from database import Database
import signal
from json import loads

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


class Exchange:

    COMMAND_SPECIFIER = "cmd"

    def __init__(self, exchange_name : str, address : tuple[str, int], processes : int=1) -> None:
        self.__database = Database()
        self.__reciver = PacketTransmitter(bind=True, bind_addr=address)
        self.__pool = ThreadPoolExecutor(max_workers=processes)
        self.__name = exchange_name
        self.__address = address
        signal.signal(signal.SIGINT, self.close)

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

    def _register_user(self, d : dict) -> bool:
        '''
        register an new user
        '''
        # name : str, surname : str, email : str, password : str, fiscal_code : str, nationality : str, telephone : str
        # aggiungi utente al database
        # crea un conto in euro
        pass
    
    def _get_cookie(self, email : str, passw : str) -> str:
        '''
        return the cookie to the client
        '''
        # TODO: maneggiare una risposta indietro
        pass

    def _get_report(self, user : str):
        '''
        returns the report of the user
        '''
        # restituisci il saldo di tutti conti correnti
        pass

    def _withdraw(self, d : dict):
        '''
        withdraw fiat money 
        '''
        pass

    def _deposit(self):
        '''
        deposit fiat money
        '''
        pass

    def _send(self):
        '''
        send money to another user
        '''
        pass

    def _sell(self):
        '''
        sell a crypto
        '''
        # controlla che non ci siano ordini di compra vicini nel database, usa quelli
        # altrimetti piazzane uno
        pass

    def _buy(self):
        '''
        buy a crypto
        '''
        # controlla che non ci siano ordini di vendita vicini nel database, usa quelli
        # altrimetti piazzane uno
        pass

    def _create_wallet(self) -> str:
        '''
        create a wallet
        '''
        pass

    def _create_account_fiat(self) -> str:
        '''
        create an account that contais only fiat money
        '''
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

    def run(self):
        '''
        run the exchange,
        will handle for user connections 
        '''
        self.__database.insert_into(f"INSERT INTO running_exchanges VALUES ('{self.__name}', '{self.__address[0]}', {self.__address[1]})")
        
        while True:
            d = self.__wait_for_command()
            self.__pool.submit(d.get(self.COMMAND_SPECIFIER), d)
    
    def close(self, *arguments):
        self.__database.delete(f"DELETE FROM running_exchanges WHERE host = '{self.__address[0]}' AND port = {self.__address[1]}")
        self.__reciver.close()
        self.__database.close()
        self.__pool.shutdown(wait=True)
        exit(0)

        

if __name__ == "__main__":
    from sys import argv
    iter = iter(argv)
    next(iter)
    
    try:
    
        name = next(iter)
        
        if name == "-h":
            print("[name: (required)] [port (default 31415)] [host: (deafult localhost)] [workers (for ThreadPool): (deafult 1)]")
            exit(0)

    except StopIteration:
        print("you have to provide a name of the exchange")
        exit(0)
    
    port = next(iter, 31415)
    host = next(iter, "localhost")
    workers = next(iter, 1)
    exc = Exchange(name, (host, port), processes=workers)
    exc.run()