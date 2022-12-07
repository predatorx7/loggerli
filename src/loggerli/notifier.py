from abc import ABC, abstractmethod


class Listenable(ABC):
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def listen(self, listener):
        pass

    @abstractmethod
    def dispose(self):
        pass


class StateNotifier(Listenable):
    def __init__(self, value=None) -> None:
        self.__value = value
        self.__i = 0
        self.__listeners = dict()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, o):
        self.__value = o
        self.notifyListeners()

    def notifyListeners(self):
        for key in self.__listeners:
            try:
                self.__listeners[key](self.value)
            except Exception as e:
                print(e)

    def listen(self, listener):
        self.__listeners[self.__i] = listener
        def removeListenerCallback(): return self.__listeners.pop(self.__i)
        self.__i += 1
        return removeListenerCallback

    def dispose(self):
        self.__listeners.clear()