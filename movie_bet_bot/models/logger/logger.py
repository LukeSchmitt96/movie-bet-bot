import logging
import logging.config
from os import path

# load config
logging.config.fileConfig(path.join(path.dirname(__file__), "logger.conf"))

# create logger
Logger = logging.getLogger("MovieBetBot")

print = Logger.info
