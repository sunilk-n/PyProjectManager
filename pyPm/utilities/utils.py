import argparse
import logging
log = logging.getLogger()


class Parser(argparse.ArgumentParser):
    def error(self, message):
        log.warning(message)
        self.print_help()
