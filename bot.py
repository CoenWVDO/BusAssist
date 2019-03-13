#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, RegexHandler, Filters, ConversationHandler, CallbackQueryHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BUSSTOP, BUSTIME = range(2)

busstopstring = ''

def start(bot, update):
	keyboard = [[InlineKeyboardButton("Oerle", callback_data='Oerle'), InlineKeyboardButton("Veldhoven", callback_data='Veldhoven'),InlineKeyboardButton("Airport", callback_data='Airport')],[InlineKeyboardButton("Station", callback_data='Station')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Please choose a destination:', reply_markup=reply_markup)      
	return BUSTIME
	
def bustime(bot, update):
	logger.info("BUSSTOP: %s", busstopstring)
	keyboard = [[InlineKeyboardButton("17:00", callback_data='0'),InlineKeyboardButton("17:05", callback_data='5'),InlineKeyboardButton("17:10", callback_data='10')],[InlineKeyboardButton("17:15", callback_data='0')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('At what time you take the bus?', reply_markup=reply_markup)

	return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def button(bot, update):
	query = update.callback_query
	global busstopstring
	busstopstring = query.data
	logger.info("Busstop: %s", busstopstring)
	bot.edit_message_text(text="Selected option: {}".format(busstopstring), chat_id=query.message.chat_id, message_id=query.message.message_id)

def bustimeCalback(bot, update):
	query = update.callback_query
	global bustimetring
	bustimetring = query.data
	logger.info("Bustime: %s", bustimetring)
	bot.edit_message_text(text="Selected option: {}".format(bustimetring), chat_id=query.message.chat_id, message_id=query.message.message_id)
	

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("591074486:AAFMD3AVx7zIS7pju4196-GGltuEcCrQaQA")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states BUSSTOP, TIME
    conv_handler = ConversationHandler(entry_points=[CommandHandler("start", start)], states={ BUSTIME: [RegexHandler("" , bustime)]}, fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)
    
    dp.add_handler(CallbackQueryHandler(button))

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
