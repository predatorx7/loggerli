from __future__ import annotations


from .level import Level
from .notifier import Listenable, StateNotifier
from .log_record import LogRecord

defaultLevel = Level.INFO

_loggers = dict()
hierarchicalLoggingEnabled = False


class imdict(dict):
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class Logger(object):
    __create_key = object()

    def __init__(self, create_key=None, name: str = None, parent: Logger = None, children: dict = None) -> None:
        assert(create_key == Logger.__create_key), \
            "Logger must be created using Logger.create"
        self.name = name
        self.parent = parent
        self.__children = children
        self.children = imdict(children)
        self.__level = None
        if (parent == None):
            self.__level = defaultLevel
        else:
            parent.__children[name] = self
        self.__controller: StateNotifier = None

    @staticmethod
    def root() -> Logger:
        return Logger.create('')

    @property
    def fullName(self):
        if (self.parent != None and self.parent.name != ''):
            return f'{self.parent.fullName}.{self.name}'
        return self.name

    @classmethod
    def create(cls, name='') -> Logger:
        if name not in _loggers:
            _loggers[name] = Logger.__named(cls.__create_key, name)
        return _loggers[name]

    @staticmethod
    def __named(create_key, name: str):
        indexOfDot = name.find('.')
        if (indexOfDot == 0):
            raise NameError("name shouldn't start with a '.'")
        if (name != '' and indexOfDot == len(name) - 1):
            raise NameError("name shouldn't end with a '.'")
        dot = name.rfind('.')
        parent: Logger = None
        thisName: str = None
        if (dot == -1):
            if (name != ''):
                parent = Logger.create('')
            thisName = name
        else:
            parent = Logger.create(name[0: dot])
            thisName = name[dot + 1:]
        return Logger(create_key, thisName, parent, dict())

    @property
    def level(self) -> Level:
        effectiveLevel: Level
        if (self.parent == None):
            effectiveLevel = self.__level
        else:
            if (self.__level != None):
                effectiveLevel = self.__level
            elif not hierarchicalLoggingEnabled:
                effectiveLevel = Logger.root().__level
            else:
                effectiveLevel = self.parent.level
        return effectiveLevel

    @level.setter
    def level(self, value: Level):
        if (not hierarchicalLoggingEnabled and self.parent != None):
            raise ValueError(
                "unsupported: Please set \"hierarchicalLoggingEnabled\" to true if you want to change the level on a non-root logger.")
        if (self.parent == None and value == None):
            raise ValueError(
                "unsupported: Cannot set the level to `null` on a logger with no parent.")
        self.__level = value

    @property
    def onRecord(self) -> Listenable:
        if (self.__controller == None):
            self.__controller = StateNotifier()
        return self.__controller

    def clearListeners(self):
        if (hierarchicalLoggingEnabled or self.parent == None):
            self.__controller.dispose()
        else:
            Logger.create('').clearListeners()

    def isLoggable(self, value: Level) -> bool:
        return value >= self.level

    def __publish(self, record: LogRecord):
        self.__controller.value = record

    def log(self, logLevel: Level, message, error=None, stackTrace=None):
        object = None
        if (self.isLoggable(logLevel)):
            if callable(message):
                message = message()
            msg: str
            if (isinstance(message, str)):
                msg = message
            else:
                msg = str(message)
                object = message
            record = LogRecord(logLevel, msg, self.fullName,
                               error, stackTrace, object,)
            if (self.parent == None):
                self.__publish(record)
            elif (not hierarchicalLoggingEnabled):
                Logger.root().__publish(record)
            else:
                target: Logger = self
                while (target != None):
                    target.__publish(record)
                    target = target.parent

    def finest(self, message, error=None, stackTrace=None):
        return self.log(Level.FINEST, message, error, stackTrace)

    def finer(self, message, error=None, stackTrace=None):
        return self.log(Level.FINER, message, error, stackTrace)

    def fine(self, message, error=None, stackTrace=None):
        return self.log(Level.FINE, message, error, stackTrace)

    def config(self, message, error=None, stackTrace=None):
        return self.log(Level.CONFIG, message, error, stackTrace)

    def info(self, message, error=None, stackTrace=None):
        return self.log(Level.INFO, message, error, stackTrace)

    def warning(self, message, error=None, stackTrace=None):
        return self.log(Level.WARNING, message, error, stackTrace)

    def severe(self, message, error=None, stackTrace=None):
        return self.log(Level.SEVERE, message, error, stackTrace)

    def shout(self, message, error=None, stackTrace=None):
        return self.log(Level.SHOUT, message, error, stackTrace)
