import configparser
from pathlib import Path


class ConfigReader(object):
    __slots__ = []

    _parser: configparser.ConfigParser = configparser.ConfigParser()

    def __new__(cls, *args, **kwargs):
        # 单例模式
        if not hasattr(ConfigReader, '_instance'):
            ConfigReader._instance = super().__new__(cls)
        return ConfigReader._instance

    def __init__(self,
                 ini_file: Path = Path(__file__).parent.parent / Path('data_file/config.ini')):
        self._parser.read(str(ini_file))

    def get_database_URL(self) -> str:
        """
        获取数据库链接

        :return:database_URL
        """
        return self._parser.get('databaseURL', 'url')

# if __name__ == '__main__':
#     c = ConfigReader()
#     print(c.get_database_URL())
