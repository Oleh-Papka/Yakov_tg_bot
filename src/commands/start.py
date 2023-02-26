from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from src.crud.user import create_or_update_user
from src.utils import escape_md2_no_links
from src.utils.db_utils import get_session


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Create a new user instance and add it to the database
    async with get_session() as session:
        await create_or_update_user(session, user)

    msg = (f"Привіт {user.first_name}, я Yakov і створений тому, що моєму [розробнику]"
           "(tg://user?id={Config.CREATOR_ID}) було нудно.\nЯ постійно отримую апдейти "
           "та нові функції, залишайся зі мною, розробнику приємно, а тобі цікаві фішки 🙃\n\n"
           "Підказка - /help\n\nP.S. Підтримати ЗСУ можна [тут]"
           "(https://savelife.in.ua/donate/#payOnce), Слава Україні!")

    await update.message.reply_text(escape_md2_no_links(msg),
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    disable_web_page_preview=True)


start_command_handler = CommandHandler('start', start)
