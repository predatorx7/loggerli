
from src.loggerli.level import Level
from src.loggerli.logger import Logger

logger = Logger.create()

Logger.root().level = Level.ALL  # defaults to Level.INFO

logger.on_record.listen(lambda v: print(f'log {v}'))

logger.info('hello world')

hello = Logger.create('hello')

Logger.hierarchical_logging_enabled = True

hello.level = Level.ALL

hello.info("Hello")

world = hello.child('world')

world.on_record.listen(lambda v: print(f'log from world {v}'))

world.info("World")
