from SavingAndReporting.Saving.schemas.account import Account
from SavingAndReporting.Saving.controllers.historic_controller import HistoricController

class AccountController:
    @staticmethod
    def create_account(account_id: str,
                       initial_amount=float,
                       type_of_account=str) -> Account:
        account = Account(account_id=account_id, initial_amount=initial_amount, type_of_account=type_of_account)
        account.save()
        HistoricController.create_historic_table(account)
        return account

    @staticmethod
    def get_account(account_id: str):
        try:
            return Account.get(Account.account_id == account_id)
        except Account.DoesNotExist:
            return None


    @staticmethod
    def erase_account(account_id: str):
        # Check if the account exists
        account = AccountController.get_account(account_id)
        if account is None:
            return {"message": "Account does not exist."}

        # Delete the account
        account.delete_instance()

        # Erase the associated historic table
        HistoricController.erase_historic_table(account_id)

        return {"message": "Account and associated historic table erased successfully."}

    @staticmethod
    def get_all_accounts():
        accounts = Account.select().execute()
        account_data = [account for account in accounts]
        return account_data
