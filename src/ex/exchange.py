from multiprocessing.pool import ThreadPool

class Exchange:
    def __init__(self) -> None:
        pass

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

    def _register_user(self, name : str, surname : str, email : str, password : str, fiscal_code : str, nationality : str, telephone : str) -> bool:
        '''
        register an new user
        '''
        pass

    def _withdraw(self, atm_id : str):
        '''
        withdraw fiat money 
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
        pass

    def _buy(self):
        '''
        buy a crypto
        '''
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