import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler, ContextTypes
from telegram.ext.filters import PHOTO, TEXT

TOKEN = '6967769063:AAHwwWnsp8xtkQRw5O1dtU0zwrXnDJzEMvg'

POSTER, TITLE, CAST, RELEASE_DATE, RATING, DOWNLOAD_LINK = range(6)

movie_data = {}

# Define authorized users by their usernames (without '@') and user IDs
AUTHORIZED_USERS = {
    'i_am_yamraj': 1837294444,  # Replace with actual user ID
    'likehanuman': 7138890729,  # Replace with actual user ID
}

def is_authorized(user):
    return (user.username and user.username.lower() in AUTHORIZED_USERS) or (user.id in AUTHORIZED_USERS.values())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    print(f"User attempting to access: ID={user.id}, Username={user.username}")
    if not is_authorized(user):
        await update.message.reply_text("Sorry, you are not authorized to use this bot. This bot is developed by @i_am_yamraj. Please contact him to access or to make a pay bot.")
        return ConversationHandler.END
    
    await update.message.reply_text("Welcome! Let's create a movie post. Please send the movie poster image.")
    return POSTER

async def poster(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo = update.message.photo[-1]
    movie_data['poster_file_id'] = photo.file_id
    await update.message.reply_text("Great! Now, please enter the movie title.")
    return TITLE

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    movie_data['title'] = update.message.text
    await update.message.reply_text("Please enter the cast names.")
    return CAST

async def cast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    movie_data['cast'] = update.message.text
    await update.message.reply_text("Please enter the release date.")
    return RELEASE_DATE

async def release_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    movie_data['release_date'] = update.message.text
    await update.message.reply_text("Please enter the movie rating.")
    return RATING

async def rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    movie_data['rating'] = update.message.text
    await update.message.reply_text("Please enter the download link.")
    return DOWNLOAD_LINK

async def download_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    movie_data['download_link'] = update.message.text
    await send_movie_post(update, context)
    return ConversationHandler.END

async def send_movie_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "⊱ ────── {⋅. ✯ .⋅} ────── ⊰\n"
        "*By @NeonGhost_Network*\n"
        "⊱ ────── {⋅. ✯ .⋅} ────── ⊰\n\n"
        f"*🎬 Title:* {movie_data['title']}\n\n"
        f"*🌟 Cast:* {movie_data['cast']}\n\n"
        f"*📅 Release Date:* {movie_data['release_date']}\n\n"
        f"*⭐️ Rating:* {movie_data['rating']}\n\n"
        f"*📥 Download:* [Download Movie]({movie_data['download_link']})"
    )

    keyboard = [
        [InlineKeyboardButton("𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 🍿🎬", url="https://t.me/+frnRoqV3_5YzNWU0")],
        [InlineKeyboardButton("𝙇𝙚𝙖𝙠 𝙈𝙈𝙎 𝙑𝙞𝙙𝙚𝙤𝙨 (‿ˠ‿) 🍑👈🤤", url="https://t.me/+8xrQArpgezc0YTdk")],
        [InlineKeyboardButton("𝘽𝙖𝙘𝙠𝙪𝙥 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 🔙🆙", url="https://t.me/NeonGhost_Network")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=movie_data['poster_file_id'],
        caption=caption,
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            POSTER: [MessageHandler(PHOTO, poster)],
            TITLE: [MessageHandler(TEXT & ~PHOTO, title)],
            CAST: [MessageHandler(TEXT & ~PHOTO, cast)],
            RELEASE_DATE: [MessageHandler(TEXT & ~PHOTO, release_date)],
            RATING: [MessageHandler(TEXT & ~PHOTO, rating)],
            DOWNLOAD_LINK: [MessageHandler(TEXT & ~PHOTO, download_link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == '__main__':
    main()
