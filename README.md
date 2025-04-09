![](https://capsule-render.vercel.app/api?type=waving&height=200&color=gradient&text=rainbow_logging&animation=fadeIn)

🌈 A flexible and minimal Python logging utility that adds colorful, readable log output to your terminal.

<p align="center">
  <img width="128" height="128" src="assets/rainbow_logging.png">
</p>

## Installation

```bash
pip install rainbow_logging
```

## Usage

To import both the rainbow_logging and the basic logging module, you can use the following import statements:

```python
from rainbow_logging import LoggingConfig, Timezone, verify
import logging
```

LoggingConfig is a class that configures how logging output will be displayed.
It can be used as shown below:

```python
LoggingConfig.set_level(LoggingConfig.DEBUG).thread_name(True).traceback(False).asctime(True).finish(Timezone.Asia.Seoul)
```

* `LoggingConfig`
    * `levelname`: If set to True, the logging level will be displayed. If False, it will be omitted.
    * `asctime`: If set to True, timestamp information will be included. If False, it will be omitted.
    * `thread_name`: If set to True, it will display each thread individually in a multi-threaded environment. If False, output will be the same across threads.
    * `set_level`: Determines from which level logs will be displayed. The following values can be used: `LoggingConfig.DEBUG`, `LoggingConfig.INFO`, `LoggingInfo.WARNING`, `LoggingInfo.ERROR`, `LoggingInfo.CRITICAL`
    * `traceback`: If True, traceback information will be displayed when a CRITICAL level log occurs.
    * `save_file`: If a filename is provided, logs will be saved to the file in addition to being output to stdout.
    * `finish`: Takes a Timezone as an argument and completes all configurations. (This must be called at the end for all settings to be applied.)

* `Timezone`
    * This class is used as an argument for LoggingConfig, for example: `Timezone.America.Cambridge_Bay`

### Example

```python
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
```
![](https://capsule-render.vercel.app/api?type=waving&height=200&color=gradient&text=rainbow_logging&animation=fadeIn&section=footer)