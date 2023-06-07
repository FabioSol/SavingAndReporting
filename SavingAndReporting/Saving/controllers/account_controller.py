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
    def get_account(account_id: str) -> Account:
        try:
            return Account.get(Account.account_id == account_id)
        except Account.DoesNotExist:
            return None
