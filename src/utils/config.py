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
    config = configparser.ConfigParser()
    configfile = __file__.replace('config.py', 'config.ini')
    config.read(configfile, 'UTF-8')
    # DEFAULTセクションのみバケット名の後ろにUSER名を付加
    if(env == 'DEFAULT'):
        bucket_name = config['DEFAULT'].get('BUCKET_NAME')
        dev_database = config['DEFAULT'].get('ATHENA_DB_NAME')
        user = os.environ.get('USER')
        config.set('DEFAULT', 'BUCKET_NAME', bucket_name + '.' + user)
        config.set('DEFAULT', 'ATHENA_DB_NAME', dev_database + '_' + user)
        config.set('DEFAULT', 'ATHENA_RESULT_BUCKET', bucket_name + '.' + user)
        config.set('DEFAULT', 'ATHENA_DATA_BUCKET', bucket_name + '.' + user)
    return config[env]
