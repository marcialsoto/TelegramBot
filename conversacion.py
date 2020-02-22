import logging
import random

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

TOKEN = '1042218907:AAFEDUxtW4roSOaAzOBg55hsNFntVborls4'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

EMOTION, HAPPEN, DO, DOING, PHOTO, LOCATION, BIO = range(7)

def start(update, context):
    user = str(update.message.from_user.first_name)
    reply_keyboard = [['😁', '😔', '😡']]

    update.message.reply_text(
        '¡Hola ' + user + '! Mi nombre es Felícita y voy a conversar contigo. '
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
    
    elif update.message.text == '😡':
        update.message.reply_text('¡Bájale un poco a las revoluciones, ' + str(user.first_name) + '! Cuéntame un poco más...')

        return HAPPEN

    return PHOTO


def happen(update, context):
    user = update.message.from_user
    message = update.message.text.upper()

    if("TRABAJO" in message):
        reply_keyboard = [['Descansar', 'Encontrar otro', 'No lo sé']]

        update.message.reply_text(
            str(user.first_name) + ' eso está mal 😔'
            'Pero vamos, hay muchas cosas que podemos hacer al respecto, cuéntame, ¿qué te gustaría hacer?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    elif("DISCUTÍ" in message):
        update.message.reply_text('Peleamos desde tiempos inmemoriables, pero un mundo de paz solo se contruye con justicia. Dale tiempo y pelea por una reconciliación.')
        return ConversationHandler.END
    
    elif("APARIENCIA" in message):
        update.message.reply_text('Francamente lo dudo, pero envíame una foto para estar seguros')
        return PHOTO
    
    elif("NADIE" in message):
        update.message.reply_text('Eso no es cierto, mándame tu ubiación y estoy eontigo en un abrir y cerrar de ojos...')
        return LOCATION
    
    else:
        update.message.reply_text('Como dice Silvito el Libre, "lo que un día te quita el aliento, al otro no está ni en tu cabeza"')
        return ConversationHandler.END

    logger.info("DISCUTÍ" in message)
    return DO

def do(update, context):
    user = update.message.from_user
    message = update.message.text.upper()
    reply_keyboard = [['Viajar', 'Aprender', 'Conocer', 'Descubrir']]

    if update.message.text == 'Descansar':
        update.message.reply_text(
            str(user.first_name) + ' me parece perfecto. Descansar luego de una experiencia así es lo que se recomienda en estos casos.'
            'Puedes tomarte el tiempo que te sea necesario antes de volver al ruedo. Te puedo recomendar las siguientes actividades:',
            
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    elif update.message.text == 'Encontrar otro':
        update.message.reply_text( str(user.first_name) + ', entiendo. Quizá debamos empezar por actualizar tu LinkedIn https://pe.linkedin.com/')
        
        return ConversationHandler.END
    
    elif update.message.text == 'No lo sé':
        update.message.reply_text( str(user.first_name) + ', entiendo por lo que estás pasando. Lo peor que puedes hacer es darlo muchas vueltas, ¿qué te parece si descansamos un poco? Escuchemos un poco de tu música favorita https://music.youtube.com/playlist?list=PLqtAv5lCZ8wVtCFK7oMpdp6sxGxx9Qi5O')
        
        return ConversationHandler.END
            
    
    return DOING

def doing(update, context):
    user = update.message.from_user
    message = update.message.text.upper()
    
    if update.message.text == 'Viajar':
        update.message.reply_text('¡' + str(user.first_name) + ', excelente! ¿Qué te parece si revisamos las mejores ofertas en viajes al interior del país? https://www.despegar.com.pe/',
                                reply_markup=ReplyKeyboardRemove())
    
    elif update.message.text == 'Aprender':
        update.message.reply_text('¡' + str(user.first_name) + ', excelente! Revisemos estos cursos sobre tecnología https://www.udemy.com/courses/development/',
                                reply_markup=ReplyKeyboardRemove())
    
    elif update.message.text == 'Descubrir':
        update.message.reply_text('¡' + str(user.first_name) + ', excelente! Vemos estos estrenos https://www.cineplanet.com.pe/ ',
                                reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Pues para mí te ves genial. Debes limpiar tu espejo, que está opacando tu belleza.')

    return ConversationHandler.END


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
    update.message.reply_text('Estoy yendo a verte...')

    return ConversationHandler.END


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


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
            EMOTION: [MessageHandler(Filters.regex('^(😁|😔|😡)$'), emotion),
                    CommandHandler('start', start)],

            HAPPEN: [MessageHandler(Filters.text, happen),
                    CommandHandler('start', start)],

            DO: [MessageHandler(Filters.regex('^(Descansar|Encontrar otro|No lo sé)$'), do),
                    CommandHandler('start', start)],
            
            DOING: [MessageHandler(Filters.text, doing),
                    CommandHandler('start', start)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)]
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