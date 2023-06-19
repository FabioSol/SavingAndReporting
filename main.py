from fastapi import FastAPI
from datetime import datetime
from SavingAndReporting.Saving.controllers import account_controller, historic_controller
from SavingAndReporting.Reporting.sending import send_message
import subprocess



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "SavingAndReporting!"}


@app.get("/ping")
async def check_status():
    return {"pong"}


@app.post("/account")
async def new_account(data: dict):
    account_id = data.get("account_id")
    initial_amount = data.get("initial_amount")
    type_of_account = data.get("type_of_account")
    account = account_controller.AccountController.get_account(account_id=account_id)
    if account is None:
        try:
            account_controller.AccountController.create_account(account_id=account_id,
                                                                initial_amount=initial_amount,
                                                                type_of_account=type_of_account)
            return {"message": "Account created successfully"}

        except Exception as e:
            return {"message": "Error occurred", "error": str(e)}
    else:
        return {"message": "Account already exist"}


@app.post("/account/addbar")
async def add_bar(data: dict):
    account_id = data.get("account_id")
    date_time = datetime.strptime(data.get("date_time"), "%Y.%m.%d %H:%M:%S")
    equity_open = data.get("equity_open")
    equity_high = data.get("equity_high")
    equity_low = data.get("equity_low")
    equity_close = data.get("equity_close")
    balance_open = data.get("balance_open")
    balance_high = data.get("balance_high")
    balance_low = data.get("balance_low")
    balance_close = data.get("balance_close")
    try:
        account = account_controller.AccountController.get_account(account_id=account_id)
        historic_controller.HistoricController.add_historic_row(account=account,
                                                                date_time=date_time,
                                                                equity_open=equity_open,
                                                                equity_high=equity_high,
                                                                equity_low=equity_low,
                                                                equity_close=equity_close,
                                                                balance_open=balance_open,
                                                                balance_high=balance_high,
                                                                balance_low=balance_low,
                                                                balance_close=balance_close)

        return {"message": "Data received successfully"}

    except Exception as e:
        return {"message": "Error occurred", "error": str(e)}


@app.delete("/account/{account_id}")
async def delete_account(account_id: str):
    account = account_controller.AccountController.get_account(account_id=account_id)
    if account:
        try:
            # Delete the account and its associated historic table
            account_controller.AccountController.erase_account(account_id=account_id)

            return {"message": "Account deleted successfully"}
        except Exception as e:
            return {"message": "Error occurred", "error": str(e)}
    else:
        return {"message": "Account not found"}

@app.post("/account/report")
async def report(data: dict):
    account_id = data.get("account_id")
    chat_id = data.get("chat_id")
    message = send_message(account_id,chat_id)
    return {"message": message}

@app.post("/account/test")
async def test(data: dict):
    return {"message": "done"}



def run_uvicorn():
    command = 'python -m uvicorn main:app --port 80 --reload'
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    run_uvicorn()
