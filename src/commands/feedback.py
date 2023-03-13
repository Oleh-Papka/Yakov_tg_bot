import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler, ConversationHandler, CommandHandler, ContextTypes, \
    CallbackQueryHandler

from src.config import Config
from src.crud.feedback import create_feedback, get_feedback_by_msg_id, mark_feedback_read
from src.crud.user import create_or_update_user
from src.handlers.canel_conversation import cancel, cancel_keyboard
from src.utils.db_utils import get_session
from src.utils.message_utils import escape_md2, escape_md2_no_links

FEEDBACK_START, REPLY_START = 1, 2


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message
    user = update.effective_user
    context.user_data['command_msg'] = message

    async with get_session() as session:
        await create_or_update_user(session, user)

    context.user_data['markup_msg'] = await message.reply_text('Ок, надішліть свій фідбек нижче:',
                                                               reply_markup=cancel_keyboard)

    return FEEDBACK_START


async def feedback_get_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message
    user = update.effective_user
    markup_msg = context.user_data['markup_msg']

    await markup_msg.edit_reply_markup()

    async with get_session() as session:
        await create_feedback(session, user.id, message.message_id, message.text, False)

    # Firstly send to developer feedback
    to_dev_text = f"Повідомлення від {escape_md2(user.name)}"
    to_dev_text += f"\n\n```{escape_md2(message.text)}```\n\n"
    to_dev_text += f"Відповісти на фідбек? \\(/reply\\_feedback\\_{message.message_id}\\)"
    await context.bot.send_message(Config.OWNER_ID, text=to_dev_text, parse_mode=ParseMode.MARKDOWN_V2)

    # Inform user that feedback sent
    to_user_text = f'✅ Шик, уже надіслав [розробнику](tg://user?id={Config.OWNER_ID})!'
    await message.reply_text(escape_md2_no_links(to_user_text), parse_mode=ParseMode.MARKDOWN_V2)

    context.user_data.clear()
    return ConversationHandler.END


async def feedback_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message
    context.user_data['command_msg'] = message

    feedback_reply_msg_id = int(message.text.replace('/reply_feedback_', ''))

    async with get_session() as session:
        feedback_model = await get_feedback_by_msg_id(session, feedback_reply_msg_id)

    if not feedback_model:
        await message.reply_text(escape_md2(f'Дивно немає фідбеку із msg_id=`{feedback_reply_msg_id}`', ['`']),
                                 parse_mode=ParseMode.MARKDOWN_V2)
        context.user_data.clear()
        return ConversationHandler.END

    context.user_data['feedback_reply_msg_id'] = feedback_reply_msg_id
    context.user_data['feedback_reply_user_id'] = feedback_model.user_id

    name = escape_md2(feedback_model.user.first_name)

    response_text = (f'Пишемо відповідь на фідбек користувача '
                     f'[{name}](tg://user?id={feedback_model.user.id}):'
                     f'\n\n```{feedback_model.msg_text}```\n\n')

    context.user_data['markup_msg'] = await message.reply_markdown_v2(escape_md2_no_links(response_text, ['`']),
                                                                      reply_markup=cancel_keyboard)

    return REPLY_START


async def feedback_reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message
    text = message.text

    feedback_reply_msg_id = context.user_data['feedback_reply_msg_id']
    feedback_reply_user_id = context.user_data['feedback_reply_user_id']
    markup_msg = context.user_data['markup_msg']

    response_text = f"У відповідь на ваше повідомлення розробник пише:\n\n"
    response_text += f"{escape_md2(text)}\n\n"
    response_text += f"Ще раз дякую за фідбек 🙃"

    await markup_msg.edit_reply_markup()

    await context.bot.send_message(chat_id=feedback_reply_user_id,
                                   text=response_text,
                                   parse_mode=ParseMode.MARKDOWN_V2,
                                   reply_to_message_id=feedback_reply_msg_id)

    async with get_session() as session:
        await mark_feedback_read(session, feedback_reply_msg_id)

    await message.reply_text('✅ Чудово, я уже відповів користувачу!')

    context.user_data.clear()
    return ConversationHandler.END


feedback_handler = ConversationHandler(
    entry_points=[CommandHandler('feedback', feedback)],
    states={
        FEEDBACK_START: [
            CallbackQueryHandler(cancel, pattern='^cancel$'),
            MessageHandler(filters.Regex(re.compile(r'^/cancel$')), cancel),
            MessageHandler(filters.TEXT, feedback_get_user_text)
        ]
    },
    fallbacks=[
        MessageHandler(filters.ALL, cancel)
    ],
    conversation_timeout=300.0
)

feedback_reply_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(re.compile(r'/reply_feedback_\d+')), feedback_reply)],
    states={
        REPLY_START: [
            CallbackQueryHandler(cancel, pattern='^cancel$'),
            MessageHandler(filters.Regex(re.compile(r'^/cancel$')), cancel),
            MessageHandler(filters.TEXT, feedback_reply_text)
        ]
    },
    fallbacks=[
        MessageHandler(filters.ALL, cancel)
    ],
    conversation_timeout=300.0
)
