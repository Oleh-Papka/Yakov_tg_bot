from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes, CommandHandler

from crud.user import create_or_update_user, get_user_by_id
from utils import escape_md2_no_links
from utils.db_utils import get_session
from utils.message_utils import send_upload_photo_action
from utils.time_utils import UserTime
from utils.weather_utils import OpenWeatherMapAPI, ScreenshotAPI


@send_upload_photo_action
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    user = update.effective_user

    async with get_session() as session:
        await create_or_update_user(session, user)

        user_model = await get_user_by_id(session, user.id)
        users_city_model = user_model.city

    if not users_city_model:
        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        error_text = ('⚠ Схоже місто для прогнозу погоди не налаштовано!\n '
                      'Якщо не вказати міста я не знаю, що відповісти на команду.\n\n'
                      'Для налаштування міста обери відповідний пункт у налаштуваннях - /settings')
        await message.reply_text(error_text)
        return

    user_time = UserTime(offset=user_model.timezone_offset)

    if user_time.next_day_flag:
        date = user_time.tomorrow.date_repr()
    else:
        date = user_time.date_repr()

    if sinoptik_url := users_city_model.sinoptik_url:
        if picture := ScreenshotAPI.get_photo(sinoptik_url, date):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)

            date_verbose = 'завтра' if user_time.next_day_flag else 'сьогодні'
            took_from_text = (f'Погода {users_city_model.local_name}, {date_verbose}\('
                              f'{user_time.date_repr(True)}\), взяв [тут]({sinoptik_url}).')

            caption = escape_md2_no_links(took_from_text)
            await message.reply_photo(picture.content, caption=caption, parse_mode=ParseMode.MARKDOWN_V2)
            return

    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    weather_text = OpenWeatherMapAPI.compose_msg(users_city_model, user_time)
    await message.reply_markdown_v2(escape_md2_no_links(weather_text), disable_web_page_preview=True)


weather_command_handler = CommandHandler('weather', weather)


async def weather_callback(context: ContextTypes.DEFAULT_TYPE):
    async with get_session() as session:
        user_model = await get_user_by_id(session, context.job.chat_id)
        users_city_model = user_model.city

    if not users_city_model:
        error_text = ('⚠ Схоже місто для прогнозу погоди не налаштовано!\n '
                      'Якщо не вказати міста я не знаю, що відповісти на команду.\n\n'
                      'Для налаштування міста обери відповідний пункт у налаштуваннях - /settings')
        await context.bot.send_message(chat_id=context.job.chat_id,
                                       text=error_text)
        return

    user_time = UserTime(offset=user_model.timezone_offset)

    if user_time.next_day_flag:
        date = user_time.tomorrow.date_repr()
    else:
        date = user_time.date_repr()

    if sinoptik_url := users_city_model.sinoptik_url:
        if picture := ScreenshotAPI.get_photo(sinoptik_url, date):
            date_verbose = 'завтра' if user_time.next_day_flag else 'сьогодні'
            took_from_text = (f'Погода {users_city_model.local_name}, {date_verbose}\('
                              f'{user_time.date_repr(True)}\), взяв [тут]({sinoptik_url}).')

            caption = escape_md2_no_links(took_from_text)
            await context.bot.send_photo(chat_id=context.job.chat_id,
                                         photo=picture.content,
                                         caption=caption,
                                         parse_mode=ParseMode.MARKDOWN_V2)
            return

    weather_text = OpenWeatherMapAPI.compose_msg(users_city_model, user_time)

    await context.bot.send_message(chat_id=context.job.chat_id,
                                   text=escape_md2_no_links(weather_text),
                                   disable_web_page_preview=True,
                                   parse_mode=ParseMode.MARKDOWN_V2)
