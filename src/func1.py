import requests

from utils.config import get_config
from utils.logger import get_logger

# 環境定数
conf = get_config()
# ロガー
logger = get_logger('wfrpt', conf.get('LOG_LEVEL'))


def lambda_handler(event, context):
    """ lambda handler

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


if __name__ == "__main__":
    target_url = conf.get('API_URL')
    ret = lambda_handler({'url': target_url}, '')
