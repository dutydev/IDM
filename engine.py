from dutymanager.core.main import Core
from module.utils.logger import logger

bot = Core(use_ngrok=False)
logger.info("Bot has been started!")

if __name__ == '__main__':
    bot.run()