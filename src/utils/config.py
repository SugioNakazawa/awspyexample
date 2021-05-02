import os
import configparser


def get_config():
    env = os.environ.get('WFR_ENV', 'DEFAULT')
    inifile = configparser.ConfigParser()
    configfile = __file__.replace('config.py', 'config.ini')
    inifile.read(configfile, 'UTF-8')
    return inifile[env]


if __name__ == '__main__':
    print(get_config().get('BUCKET_NAME'))
