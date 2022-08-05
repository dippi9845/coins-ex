from multiprocessing.pool import ThreadPool

class Exchange:
    def __init__(self) -> None:
        pass

    def register_user(self, name : str, surname : str, email : str, password : str, fiscal_code : str, nationality : str, telephone : str) -> bool:
        '''
        register an new user
        '''
        pass

    def withdraw(self, atm_id : str):
        '''
        withdraw fiat money 
        '''
        pass

    def send(self):
        '''
        send money to another user
        '''
        pass

    def _make_transaction(self):
        '''
        perform a generic transaction
        '''
        pass

    def sell(self):
        '''
        sell a crypto
        '''
        pass

    def buy(self):
        '''
        buy a crypto
        '''
        pass

    def _create_account(self) -> str:
        '''
        create a generic account wallet / account fiat
        '''
        pass

    def create_wallet(self) -> str:
        '''
        create a wallet
        '''
        pass

    def create_account_fiat(self) -> str:
        '''
        create an account that contais only fiat money
        '''
        pass