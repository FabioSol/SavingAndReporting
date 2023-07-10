from config import telegram_token
from SavingAndReporting.Reporting.images import make_image
from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
from SavingAndReporting.Saving.controllers.account_controller import AccountController
from telegram import Bot
import asyncio
from SavingAndReporting import imgs_path
import re


def send_message(account_id: str, chat_id: str):
    make_image(account_id)
    last_day = HistoricController.get_last_24hrs_historic_rows(account_id)

    equity_open = last_day[0].get("equity_open")
    equity_close = last_day[-1].get("equity_close")
    balance_open = last_day[0].get("balance_open")
    balance_close = last_day[-1].get("balance_close")
    account = AccountController.get_account(account_id)
    currency = re.findall(r"\((.*?)\)", account.type_of_account)[0]
    caption = f'<b>Account:</b>     {account_id} \n' + \
              f'<b>Balance:</b>      ${"{:,.2f}".format(balance_close)} {currency} ({round(balance_close / balance_open - 1, 2)}%) \n' + \
              f'<b>Equity:</b>         ${"{:,.2f}".format(equity_close)} {currency} ({round(equity_close / equity_open - 1, 2)}%)'
    asyncio.ensure_future(async_send(imgs_path, account_id, caption, chat_id))
    return {"message": [account_id, chat_id]}


async def async_send(img_path, account_id, caption, chat_id):
    bot = Bot(token=telegram_token)
    try:
        with open(img_path + account_id + ".png", "rb") as image_file:
            await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption, parse_mode='HTML')
        return True
    except:
        return False
