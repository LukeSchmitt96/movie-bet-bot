import logging
import logging.config
from os import path

# load config
fileName = path.join(
    path.split(path.dirname(path.abspath(__file__)))[0], "logger", "logger.conf"
)
logging.config.fileConfig(fileName)

# create logger
Logger = logging.getLogger("MovieBetBot")

print = Logger.info
