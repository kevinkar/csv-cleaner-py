#
# Transaction CSV Cleaner
#
# Version 1.0.0
# 2025-01-29
#

import logging
import sys

'''
## Simple wrapper for setting up a logging handler.
'''
class Logger:

    _logger: logging.Logger

    def __init__(self, show_debug: bool = False):
        """
        Create a logger
        :param show_debug:
        """
        self._logger = logging.getLogger(__name__)
        log_level = logging.DEBUG if show_debug else logging.INFO
        self.__setup_logging(log_level)
        ## "Redirect" the calls to the logger
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.critical = self._logger.critical
        return

    def __setup_logging(self, log_level: int):
        """
        Sets up the log handler and levels
        :param log_level:
        :return:
        """
        streamhandler = logging.StreamHandler(sys.stdout)
        streamhandler.setLevel(log_level)
        streamhandler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self._logger.addHandler(streamhandler)
        self._logger.setLevel(log_level)
        return
