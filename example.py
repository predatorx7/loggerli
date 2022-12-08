
from src.loggerli.level import Level
from src.loggerli.logger import Logger

logger = Logger.create()

Logger.root().level = Level.ALL  # defaults to Level.INFO

logger.onRecord.listen(lambda v: print(f'log {v}'))

logger.info('hello world')


hello = Logger.create('hello')

Logger.hierarchicalLoggingEnabled = True

hello.level = Level.ALL

hello.info("Hello")
