from .level import Level
from datetime import datetime

_nextNumber = 0


class LogRecord:
    def __init__(self, level: Level, message: str, loggerName: str, error=None, stackTrace=None, object=None) -> None:
        self.level = level
        self.message = message
        self.loggerName = loggerName
        self.error = error
        self.stackTrace = stackTrace
        self.object = object
        self.time = datetime.now()
        global _nextNumber
        self.sequenceNumber = _nextNumber
        _nextNumber += 1

    def __str__(self):
        return f'[{self.level.name}] {self.loggerName}: {self.message}'
