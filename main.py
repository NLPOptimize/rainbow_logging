from rainbow_logging import LoggingConfig, Timezone, verify
import logging

if __name__ == '__main__':
    LoggingConfig.set_level(LoggingConfig.DEBUG).thread_name(True).traceback(False).asctime(True).finish(Timezone.Asia.Seoul)
    logging.debug('This message is a log message.')
    logging.info('This message is a log message.')
    logging.warning('This message is a log message.')
    logging.error('This message is a log message.')
    logging.critical('This message is a log message.')

    verify("1 > 2")
    Timezone.America.Cambridge_Bay
