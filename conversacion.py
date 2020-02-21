import logging
import random
import emoji

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

TOKEN = '1042218907:AAFEDUxtW4roSOaAzOBg55hsNFntVborls4'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

EMOTION, HAPPEN, PHOTO, LOCATION, BIO = range(5)

# happy = emoji.emojize("yummy :cake:", use_aliases=True)


def start(update, context):
    user = str(update.message.from_user.first_name)
    reply_keyboard = [['😁', '😔', '😭', '😡']]

    update.message.reply_text(
        '¡Hola ' + user + '!'
        'Mi nombre es Felícita y voy a conversar contigo. '
        'Cuéntame, ¿Cómo te sientes hoy?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return EMOTION


def emotion(update, context):
    user = update.message.from_user
    logger.info("Emotion of %s: %s", user.first_name, update.message.text)

    if update.message.text == '😁':
        videoList = ['https://www.youtube.com/watch?v=tmvDgUBoBSQ','https://www.youtube.com/watch?v=B6u4JNOo73k','https://www.youtube.com/watch?v=d5QeZ5INOWw']
        
        update.message.reply_text('La vida es hermosa, ' + str(user.first_name) + '😁. Puedes buscarme cuando estés triste otro día. Por mientras mira este video de gatitos: ' + random.choice(videoList))

        return ConversationHandler.END

    elif update.message.text == '😔':
        update.message.reply_text('¿Qué pasó, ' + str(user.first_name) + '? Cuéntame un poco mas...')

        return HAPPEN

    return PHOTO


def happen(update, context):
    user = update.message.from_user

    if(update.message.text.upper().find("TRABAJO") > 0):
        update.message.reply_text("Trabajar es malo")

    logger.info( update.message.text.find("trabajo") )
    update.message.reply_text("Trabajar es malo")

    return LOCATION


def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Disculpa, no entendí aquello.")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states EMOTION, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            EMOTION: [MessageHandler(Filters.regex('^(😁|😔|😭|😡)$'), emotion),
                    CommandHandler('start', start)],

            HAPPEN: [MessageHandler(Filters.text, happen),
                    CommandHandler('start', start)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    # dp.add_handler(MessageHandler(Filters.text, pizza))


    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()