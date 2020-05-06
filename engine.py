from dutymanager.core.main import Core
from dutymanager.units.tools import get_values
from module.utils.logger import logger

bot = Core(**get_values(Core))
logger.info("Bot has been started!")

if __name__ == '__main__':
    bot.run(use_ngrok=False)