import os
import configparser


def get_config():
    '''環境変数 WFR_ENV に設定された内容により定数を設定
    テスト環境：指定なし
    ステージング：STAGING
    プロダクション：PRODUCTION
    '''
    env = os.environ.get('WFR_ENV', 'DEFAULT')
    inifile = configparser.ConfigParser()
    configfile = __file__.replace('config.py', 'config.ini')
    inifile.read(configfile, 'UTF-8')
    return inifile[env]


if __name__ == '__main__':
    print(get_config().get('BUCKET_NAME'))
