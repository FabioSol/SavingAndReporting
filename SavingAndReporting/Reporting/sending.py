from config import telegram_token
from SavingAndReporting.Reporting.images import make_image
from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
from telegram import Bot
import asyncio
from SavingAndReporting import imgs_path


async def send_message(account_id: str, chat_id: str):
    make_image(account_id)
    last_bar = HistoricController.get_last_historic_row(account_id)
    equity_open = last_bar.get("equity_open")
    equity_close = last_bar.get("equity_close")
    balance_open = last_bar.get("balance_open")
    balance_close = last_bar.get("balance_close")

    caption = f'<b>Account:</b>         {account_id} \n' + \
              f'<b>Balance:</b>          {str(equity_close)} ({round(equity_close / equity_open - 1, 2)}%)\n' + \
              f'<b>Equity:</b>             {str(balance_close)} ({round(balance_close / balance_open - 1, 2)}%)'

    bot = Bot(token=telegram_token)
    with open(imgs_path + account_id + ".png", "rb") as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption, parse_mode='HTML')
    return {"message": [account_id, chat_id]}


def send_async_message(account_id: str, chat_id: str):
    return asyncio.run(send_message(account_id, chat_id))
