#
# PatPab Corporation 
# The coolest company to be in
#



from typing import Dict, List

import subprocess
import time
import logging
from Persistency import Persistency
from Belty import BeltControl

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import filters

logger: logging.Logger = logging.getLogger()

class BotCommanderAdvanced:
    def __init__(self):
        persistency: Persistency = Persistency()
        self.__root_dir : str = persistency.defaultDir()
        self.__photos_dir = self.__root_dir + "/photos"

        # Load whitelist
        whitelist_filename: str = self.__root_dir + "/belty_whitelist.txt"
        with open(whitelist_filename, "r") as file:
            self.__whitelist = set([])
            for line in file.readlines():
                self.__whitelist.add(int(line))
            print(f"Whitelist: {self.__whitelist}")

        # persistency.createDirs(self.__photos_dir)
        # Get token from configuration dir and init BotComander
        telegram_toke_file_path : str = self.__root_dir + "/belty.tk"
        if persistency.checkFileExist(telegram_toke_file_path):
            with open(telegram_toke_file_path, "r") as file:
                self.__token : str = file.read()
                self.__token = self.__token.replace('\n', '')
                self.__token = self.__token.replace('', '')
                self.__updater : Updater = Updater(self.__token, use_context=True)
                
                self.__prepareCommands()
                logger.info(f"Found Telegram token starting with {self.__token[:4]}")

                # Init belty
                self.__ctl: BeltControl = BeltControl()

                

        else:
            logger.critical("{telegram_toke_file_path} file missing. Please place your " +
                              "telegram token in that file before starting the application")
    
    def run(self):
        self.__updater.start_polling()
    
    def __prepareCommands(self):        
        handler = MessageHandler(filters.Filters.all, self.handleMsg)
        self.__updater.dispatcher.add_handler(handler)


    def handleMsg(self, update: Update, context: CallbackContext):
        message : str= update.message.text
        userid : int = update.message.from_user["id"]
        chatid : int = update.message.chat_id

        if message is not None:
            if message.startswith('/'): 
                if userid in self.__whitelist:
                    # If it is a command, execute it
                    self.__parseCommand(userid, chatid, message, update, context)
                else:
                    update.message.reply_text(f"Userid {userid} is not in whitelist")
            else:
                # Not a command
                update.message.reply_text("Please, send a valid command. Type /help for more info.")
        

    def __parseCommand(self, userid : int, chatid : int, command: str, update: Update, context: CallbackContext):
        if command == "/help":
            self.__help(update, context)
        elif command.startswith("/left"):
            tokens = command.split(' ')
            try:
                seconds = int(tokens[1])
                update.message.reply_text(f"Moving {seconds} seconds to left")
                self.__ctl.left()
                time.sleep(seconds)
                self.__ctl.stop()
            except:
                update.message.reply_text("Failed getting seconds to move")
        elif command.startswith("/right"):
            tokens = command.split(' ')
            try:
                seconds = int(tokens[1])
                update.message.reply_text(f"Moving {seconds} seconds to right")
                self.__ctl.right()
                time.sleep(seconds)
                self.__ctl.stop()
            except:
                update.message.reply_text("Failed getting seconds to move")
        elif command == "/photo":
            self.__photo(chatid, update, context)
        else:
            update.message.reply_text("Unknown command")


    def __help(self, update: Update, context: CallbackContext):
        update.message.reply_text("""
        This is a bot for webscraping houses! Available commands are
        /left N. Move N seconds to left.
        /right N. Move N seconds to right.
        /photo. Take a foto and send it.
        """)
        
    def __photo(self, chatid : int,  update: Update, context: CallbackContext):
        update.message.reply_text("Trying to take a picture, wait some seconds")
        filename = self.__photos_dir + "/" +time.strftime("%Y.%m.%d_%H.%M.%S_")+"_belty.jpg"
        result = subprocess.run(["libcamera-still", "--hflip", "--vflip", "-o", filename], capture_output=True)

        # Generate image
        if result.returncode == 0:
            context.bot.send_photo(chatid, photo=open(filename, 'rb'))

    def __checkWhitelist(self):
        pass

