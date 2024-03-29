import logging
import sys
from warnings import filterwarnings

import pytz
from loguru import logger
from telegram.ext import Defaults
from telegram.warnings import PTBUserWarning

from utils.env_utils import load_env_variable


class Config:
    ###########################################################################
    #                         Set up env vars below ⬇                         #
    ###########################################################################
    DEBUG_FLAG = bool(load_env_variable('DEBUG_FLAG', int))  # Enables debug level logging

    BOT_TOKEN = load_env_variable('BOT_TOKEN')  # Your Telegram bot token

    OWNER_ID = load_env_variable('OWNER_ID', int)  # Bot owner Telegram id
    TESTER_ID = load_env_variable('TESTER_ID', int, False)  # Bot tester Telegram id

    DEVELOPER_GH_PROFILE = load_env_variable('DEVELOPER_GH_PROFILE')
    BOT_GH_REPO = load_env_variable('BOT_GH_REPO')

    CMC_API_TOKEN = load_env_variable('CMC_API_TOKEN')  # CoinMarketCup API token
    SCREENSHOT_API_TOKEN = load_env_variable('SCREENSHOT_API_TOKEN')  # Screenshot api token
    OWM_API_TOKEN = load_env_variable('OWM_API_TOKEN')  # OpenWeatherMap API token
    BINANCE_API_TOKEN = load_env_variable('BINANCE_API_TOKEN')  # Binance API token
    BINANCE_API_PRIVAT_TOKEN = load_env_variable('BINANCE_API_PRIVAT_TOKEN')  # Binance privat API token

    DB_URL = load_env_variable('DB_URL')  # URL to your db

    BOT_DEFAULTS = Defaults(tzinfo=pytz.timezone('Europe/Kyiv'))  # Update for your timezone

    ###########################################################################
    #               Heroku hosting only. Currently unsupported!               #
    ###########################################################################
    WEBHOOK_FLAG = bool(load_env_variable('WEBHOOK_FLAG', int))  # Enables webhooks
    BOT_LINK = load_env_variable('BOT_LINK', raise_if_none=WEBHOOK_FLAG)
    # Heroku dynamically allocates application port and sets it to `PORT` env var
    BOT_PORT = load_env_variable('PORT', int, raise_if_none=WEBHOOK_FLAG)

    ###########################################################################
    #                        Do not change line below ⬇                       #
    ###########################################################################
    CREATOR_ID = 514328460  # Please credit the author (olegpapka2@gmail.com)

    SPACING = '⠀⠀⠀'  # Main whitespace characters used in formatting

    BOT_VERSION = 'v0.2.2'

    BOT_COMMANDS = [
        ('weather', 'Погода', False),
        ('crypto', 'Трішки про крипту', False),
        ('currency', 'Дані по валюті', False),
        ('ruloss', 'Втрати кацапні', False),
        ('feedback', 'Надіслати відгук', False),
        ('rep_action', 'Повторювані події', False),
        ('settings', 'Налаштування', False),
        ('tip_developer', 'Тестові донейти', False),
        ('message_users', 'Повідомити користувачів', True),
        ('help', 'Підказка', False)
    ]

    FEEDBACK_REPLY_COMMAND = '/reply_to_'

    logging_lvl = logging.DEBUG if DEBUG_FLAG else logging.INFO

    class InterceptLogsHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists.
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    format = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name: '
              '<20.20}</cyan> | <level>{message}</level> ')

    logger.remove()
    logger.add(sys.stderr, format=format)
    logger.level("DEBUG", color="<fg #787878>")
    logger.level("INFO", color="<fg #ffffff>")

    logging.basicConfig(handlers=[InterceptLogsHandler()], level=logging_lvl, force=True)

    if not DEBUG_FLAG:
        filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
