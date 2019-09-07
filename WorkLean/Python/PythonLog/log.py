# https://blog.csdn.net/chosen0ne/article/details/7319306

import logging  
import logging.config  

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("log1")  

logger.debug("debug message")  
logger.info("info message")  
logger.warning("warn message")  
logger.error("error message")  
logger.critical("critical message")