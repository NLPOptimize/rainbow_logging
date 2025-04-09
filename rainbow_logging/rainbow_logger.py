# Advanced Logging Module
import logging
import os
# logging.DISABLE = 100
import pytz
import datetime
import traceback
import inspect

# Reset
RESET = '\033[0m'

# Regular Colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Bold
BOLD_BLACK = '\033[1;30m'
BOLD_RED = '\033[1;31m'
BOLD_GREEN = '\033[1;32m'
BOLD_YELLOW = '\033[1;33m'
BOLD_BLUE = '\033[1;34m'
BOLD_MAGENTA = '\033[1;35m'
BOLD_CYAN = '\033[1;36m'
BOLD_WHITE = '\033[1;37m'

# Underline
UNDERLINE_BLACK = '\033[4;30m'
UNDERLINE_RED = '\033[4;31m'
UNDERLINE_GREEN = '\033[4;32m'
UNDERLINE_YELLOW = '\033[4;33m'
UNDERLINE_BLUE = '\033[4;34m'
UNDERLINE_MAGENTA = '\033[4;35m'
UNDERLINE_CYAN = '\033[4;36m'
UNDERLINE_WHITE = '\033[4;37m'

# High Intensity
INTENSITY_BLACK = '\033[0;90m'
INTENSITY_RED = '\033[0;91m'
INTENSITY_GREEN = '\033[0;92m'
INTENSITY_YELLOW = '\033[0;93m'
INTENSITY_BLUE = '\033[0;94m'
INTENSITY_MAGENTA = '\033[0;95m'
INTENSITY_CYAN = '\033[0;96m'
INTENSITY_WHITE = '\033[0;97m'


# List of timezone: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
class RainbowLogger(logging.StreamHandler):
    def __init__(self, enable_levelname=True, enable_asctime=False, enable_thread_name=False, enable_traceback=False, timezone='Asia/Seoul'):
        super().__init__()
        self.setLevel(logging.DEBUG)
        self.setFormatter(self.__LogFormatter(enable_levelname=enable_levelname,
                                              enable_asctime=enable_asctime,
                                              enable_thread_name=enable_thread_name,
                                              enable_traceback=enable_traceback,
                                              timezone=timezone))

    class __LogFormatter(logging.Formatter):
        def __init__(self, enable_levelname, enable_asctime, enable_thread_name, enable_traceback, timezone):
            self.enable_levelname = enable_levelname
            self.enable_asctime = enable_asctime
            self.enable_thread_name = enable_thread_name
            self.enable_traceback = enable_traceback
            self.timezone = timezone
            self.loglevel_length = {
                logging.DEBUG: 5,
                logging.INFO: 4,
                logging.WARNING: 7,
                logging.ERROR: 5,
                logging.CRITICAL: 8
            }

            # self.VERIFY = 1784

            def ___FORMATSPACEBACK___(format_name: str, pad_length: int):
                return f'[%({format_name})s]{" " * pad_length}: '

            def ___LEVELNAME___(loglevel):
                return ___FORMATSPACEBACK___("levelname", 8 - self.loglevel_length[loglevel]) if self.enable_levelname else ""

            ___ASCTIME___ = f'[%(asctime)s] ' if self.enable_asctime else ""
            ___THREADNAME___ = f'(%(threadName)s)' if self.enable_thread_name else ""

            __FORMAT_VERIFY = f'{___ASCTIME___}{___LEVELNAME___(logging.CRITICAL)}%(message)s <%(filename)s:%(funcName)s{___THREADNAME___}:%(lineno)d>'
            __FORMAT_DEBUG = f'{___ASCTIME___}{___LEVELNAME___(logging.DEBUG)}%(message)s <%(filename)s:%(funcName)s{___THREADNAME___}:%(lineno)d>'
            __FORMAT_INFO = f'{___ASCTIME___}{___LEVELNAME___(logging.INFO)}%(message)s'
            __FORMAT_WARNING = f'{___ASCTIME___}{___LEVELNAME___(logging.WARNING)}%(message)s'
            __FORMAT_ERROR = f'{___ASCTIME___}{___LEVELNAME___(logging.ERROR)}%(message)s <%(filename)s:%(funcName)s{___THREADNAME___}:%(lineno)d>'
            if self.enable_traceback:
                __FORMAT_CRITICAL = f'{___ASCTIME___}{___LEVELNAME___(logging.CRITICAL)}<%(pathname)s:%(funcName)s{___THREADNAME___}:%(lineno)d>\n%(message)s'
            else:
                __FORMAT_CRITICAL = f'{___ASCTIME___}{___LEVELNAME___(logging.CRITICAL)}%(message)s <%(pathname)s:%(funcName)s{___THREADNAME___}:%(lineno)d>'

            self.FORMATS = {
                logging.DEBUG: GREEN + __FORMAT_DEBUG + RESET,
                logging.INFO: BLUE + __FORMAT_INFO + RESET,
                logging.WARNING: YELLOW + __FORMAT_WARNING + RESET,
                logging.ERROR: MAGENTA + __FORMAT_ERROR + RESET,
                logging.CRITICAL: RED + __FORMAT_CRITICAL + RESET,
                # logging.FATAL: CYAN + __FORMAT_VERIFY + RESET,
            }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            # @@@ Print traceback when loglevel is CRITICAL
            if self.enable_traceback and record.levelno == logging.CRITICAL:
                record.msg += "\n" + "".join(traceback.format_exc())
            # @@@ Set timezone
            # [2023-12-17 19:28:37,296]
            formatter.formatTime = self.formatTime
            formatter.datefmt = '%Y-%m-%d %H:%M:%S'

            # record.levelname = record.levelname.center(self.levelname_pad)    # Centerpad is not pretty
            return formatter.format(record)

        def formatTime(self, record, datefmt=None):
            dt = datetime.datetime.fromtimestamp(record.created, tz=pytz.UTC).astimezone(pytz.timezone(self.timezone))
            if datefmt:
                s = dt.strftime(datefmt)
            else:
                try:
                    s = dt.isoformat(timespec='milliseconds')
                except TypeError:
                    s = dt.isoformat()
            return s


class LoggingConfig:
    __enable_levelname = True
    __enable_asctime = True
    __enable_thread_name = True
    __enable_traceback = True
    __logging_level = logging.DEBUG
    __filename = None

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @classmethod
    def levelname(cls, enable: bool):
        LoggingConfig.__enable_levelname = enable
        return cls

    @classmethod
    def asctime(cls, enable: bool):
        LoggingConfig.__enable_asctime = enable
        return cls

    @classmethod
    def thread_name(cls, enable: bool):
        LoggingConfig.__enable_thread_name = enable
        return cls

    @classmethod
    def traceback(cls, enable: bool):
        LoggingConfig.__enable_traceback = enable
        return cls

    @classmethod
    def set_level(cls, level):
        LoggingConfig.__logging_level = level
        return cls

    @classmethod
    def save_file(cls, filename: str):
        LoggingConfig.__filename = os.path.abspath(filename)
        return cls

    @classmethod
    def finish(cls, timezone: str):
        handlers = [RainbowLogger(
            enable_levelname=LoggingConfig.__enable_levelname,
            enable_asctime=LoggingConfig.__enable_asctime,
            enable_thread_name=LoggingConfig.__enable_thread_name,
            enable_traceback=LoggingConfig.__enable_traceback,
            timezone=timezone)]
        if LoggingConfig.__filename is not None:
            handlers.append(logging.FileHandler(filename=LoggingConfig.__filename))
        logging.basicConfig(level=LoggingConfig.__logging_level, handlers=handlers, force=True)
        return None


def verify(expression: str):
    if not eval(expression, globals(), locals()):
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        print(INTENSITY_CYAN + f"[VERIFY]  : ({expression}) at {filename}:{lineno}" + RESET)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, handlers=[RainbowLogger(
    #     enable_levelname=True,
    #     enable_asctime=True,
    #     enable_thread_name=False,
    #     enable_traceback=False)])

    LoggingConfig.set_level(True).asctime(False).thread_name(True).traceback(True).finish("Asia/Seoul")

    logging.debug('This message is a log message.')
    logging.info('This message is a log message.')
    logging.warning('This message is a log message.')
    logging.error('This message is a log message.')
    logging.critical('This message is a log message.')

    verify("1 > 2")

    LoggingConfig.set_level(True).asctime(True).thread_name(True).traceback(True).finish("Asia/Seoul")

    logging.debug('This message is a log message.')
    logging.info('This message is a log message.')
    logging.warning('This message is a log message.')
    logging.error('This message is a log message.')
    logging.critical('This message is a log message.')
