from configparser import ConfigParser


class Config:
    '''Utility to load constants

    The utility pulls data from the config.ini file located adjacent to this file.
    The parser ignores inline comments denotes by a '#'

    Attributes:
        config (ConfigParser): Parser that will scan through config.ini

    '''

    print('printing this out to note that the config loader was instantiated')
    config = ConfigParser(inline_comment_prefixes="#")
    config.read("swagscanner/utils/config.ini")

    @classmethod
    def consts(cls, section: str, key: str) -> str:
        '''Fetch the corresponding item in the config.ini file

        Args:
            section (str): The section in the config file you're searching in
            key (str): The constant you're searching for

        Returns:
            The corresponding constant in the config.ini file

        '''

        return cls.config.get(section, key)
