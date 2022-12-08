# Loggerli

This is a small light weight logger that provides APIs for debugging and error
logging, similar to loggers in other languages, such as the Closure JS Logger
and java.util.logging.Logger. The logs emitted can be listened by multiple
listeners.

## Initializing

By default, the loggerli package does not do anything useful with the log
messages. You must configure the logging level and add a handler for the log
messages.

Here is a simple logging configuration that logs all messages via `print`.

```python
from loggerli.logger import Logger
from loggerli.level import Level

logger = Logger.create()

Logger.root().level = Level.ALL  # defaults to Level.INFO

logger.on_record.listen(lambda record: print(f'log {record}'))

logger.info('hello world')
```

First, set the root `Level`. All messages at or above the current level are sent
to the `on_record` stream. Available levels are:

- `Level.OFF`
- `Level.SHOUT`
- `Level.SEVERE`
- `Level.WARNING`
- `Level.INFO`
- `Level.CONFIG`
- `Level.FINE`
- `Level.FINER`
- `Level.FINEST`

Then, listen on the `on_record` that returns a [Listenable] for `LogRecord`
events. The `LogRecord` class has various properties for the message, error,
logger name, and more.

## Logging messages

Create a `Logger` with a unique name to easily identify the source of the log
messages.

```python
log = Logger.create('MyClassName')
```

When logging more complex messages, you can pass a closure instead that will be
evaluated only if the message is actually logged:

```dart
log.fine(lambda: [1, 2, 3, 4, 5])
```

Available logging methods are:

- `log.shout(logged_content);`
- `log.severe(logged_content);`
- `log.warning(logged_content);`
- `log.info(logged_content);`
- `log.config(logged_content);`
- `log.fine(logged_content);`
- `log.finer(logged_content);`
- `log.finest(logged_content);`

## Installation & Usage

Install from github using git with

```
pip install git+https://github.com/predatorx7/loggerli.git#egg=loggerli
```

Once installed, you can import & use the library
```
from loggerli.logger import Logger
from loggerli.level import Level

logger = Logger.create()

logger.level = Level.ALL

logger.on_record.listen(lambda x: print(x))

logger.info("hello world")

```

If you want to use a specific commit, branch name, or something else then pass
that git reference like the below `git-reference`

```sh
pip install git+https://github.com/predatorx7/loggerli.git@git-reference#egg=loggerli
```

For example, if I want to install from the `main` branch then my command will be

```sh
pip install git+https://github.com/predatorx7/loggerli.git@main#egg=loggerli
```
