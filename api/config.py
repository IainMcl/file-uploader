"""
Read the contents of the config.ini file
"""

import configparser


class Config(object):
    """
    Read the contents of the config.ini file
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def __str__(self):
        return 'Config'

    def get(self, section, option):
        """
        Get the value of an option from a section

        :param section: str: Section name
        :param option: str: Option name
        """
        return self.config.get(section, option)
