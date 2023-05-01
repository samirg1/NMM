import logging
from collections.abc import Mapping
from typing import Any, TextIO

_DEFAULT_TERMINATOR_OPTOUT = "[!n]"


class _CustomFormatter(logging.Formatter):
    _defaultFormat = "%(message)s"
    _FORMATS = {
        logging.INFO: _defaultFormat,
        logging.ERROR: f"\033[31m[ERROR] {_defaultFormat} \033[0m",
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self._FORMATS.get(record.levelno, self._defaultFormat)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class _Logger(logging.Logger):
    def info(self, msg: object, *args: object, exc_info: Any = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None, end: str | None = None) -> None:
        if isinstance(msg, str) and end is not None:
            msg += _DEFAULT_TERMINATOR_OPTOUT + end
        return super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)


class _StreamHandler(logging.StreamHandler[TextIO]):
    def emit(self, record: logging.LogRecord) -> None:
        if _DEFAULT_TERMINATOR_OPTOUT in record.msg:
            record.msg, self.terminator = record.msg.split(_DEFAULT_TERMINATOR_OPTOUT)
        else:
            self.terminator = "\n"
        super().emit(record)


class LogManager:
    _logger: _Logger | None = None

    @classmethod
    def init(cls, *files: str):
        if cls._logger is not None:
            return
        logger = _Logger("Game", logging.DEBUG)
        formatter = _CustomFormatter()
        for file in files:
            fileHandler = logging.FileHandler(file)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        streamHandler = _StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        cls._logger = logger
        return logger

    @classmethod
    def get(cls) -> _Logger:
        if cls._logger is None:
            raise ValueError("Logger not set")
        return cls._logger
