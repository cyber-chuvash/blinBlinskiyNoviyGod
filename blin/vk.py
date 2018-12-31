import logging
import time

from vk_requests.api import API
from vk_requests.session import VKSession

from blin.config import Config


class _API(API):
    API_CALL_INTERVAL = 0.05

    def __init__(self):
        super().__init__(
            VKSession(
                    service_token=Config.vk_token,
                    api_version='5.92'),
            http_params=None)
        self.last_api_call = 0

    def __getattr__(self, item):
        cur_time = time.time()
        if cur_time - self.last_api_call < self.API_CALL_INTERVAL:
            sleep_for = self.last_api_call + self.API_CALL_INTERVAL - cur_time
            logging.debug(f'Sleeping for {sleep_for}')
            time.sleep(sleep_for)
        attr = super().__getattr__(item)
        self.last_api_call = time.time()
        return attr


API = _API()
