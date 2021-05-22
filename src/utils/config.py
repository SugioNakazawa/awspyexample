import os
import configparser


def get_config():
    '''config.iniに記載したSectionから環境変数 WFR_ENV に応じたSectionを返す。
    環境変数 WFR_ENV の値
        開発：指定なし、ステージング：STAGING、プロダクション：PRODUCTION

    Args:
        None
    
    Returns:
        環境変数 WFR_ENV に対応したSection
    '''
    env = os.environ.get('WFR_ENV', 'DEFAULT')
    inifile = configparser.ConfigParser()
    configfile = __file__.replace('config.py', 'config.ini')
    inifile.read(configfile, 'UTF-8')
    return inifile[env]
