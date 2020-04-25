from dutymanager.core.main import Bot
from module.utils.logger import logger

bot = Bot()
logger.info("Bot has been started!")

if __name__ == '__main__':
    bot.start()