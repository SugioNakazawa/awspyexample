import requests

from utils.config import get_config
from utils.mylogger import MyLogger

# 定数
conf = get_config()
# ロガー
logger = MyLogger('wfrpt')


def lambda_handler(event, context):
    """ lambda handler

    Args:
        event[url]: webAPIリクエスト先のURL
    
    Returns:
        webAPIのレスポンス・コードが200の場合:レスポンス(json)
        それ以外:response.status_code

    """
    target_url = event['url']
    logger.debug('request:' + target_url)
    response = requests.get(target_url)
    if(response.status_code == 200):
        logger.debug('status_code: {}'.format(response.status_code))
        return response.json()
    else:
        logger.error(response.status_code)
        # logger.error(response)
    return response.status_code
