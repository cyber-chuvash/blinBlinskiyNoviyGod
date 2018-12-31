import logging
import re

import requests

from blin.vk import API
from blin.config import Config
from blin.database import Database


class Receiver:
    def __init__(self):
        self.key, self.server, self.ts = self.get_long_poll_server()
        self.db = Database()

    def start_loop(self):
        while True:
            response = self.long_poll(self.server, self.key, self.ts)
            logging.debug(response)
            self.ts = response['ts']
            for update in response['updates']:
                if update['type'] == 'message_new':

                    text = strip_push(update['object']['text'], Config.group_id)

                    if text in ('+', 'on', 'вкл'):
                        self.db.add_chat(int(update['object']['peer_id']))
                        API.messages.send(peer_id=update['object']['peer_id'], message="ok", random_id=0)
                    if text in ('-', 'off', 'выкл'):
                        self.db.remove_chat(int(update['object']['peer_id']))
                        API.messages.send(peer_id=update['object']['peer_id'], message="ok", random_id=0)

    @staticmethod
    def get_long_poll_server():
        lps = API.groups.getLongPollServer(group_id=Config.group_id)
        return lps['key'], lps['server'], lps['ts']

    def long_poll(self, server, key, ts, wait=25):
        """
        Gets updates from VK Long Poll server
        :param server: str: VK Long Poll server URI returned by groups.getLongPollServer()
        :param key: str: Secret session key returned by groups.getLongPollServer()
        :param ts: int: Last event id
        :param wait: int: Seconds to wait before returning empty updates list
        :return: dict: {'ts': 00000000, 'updates': [list of updates], 'group_id': 00000000}
        """

        payload = {'act': 'a_check', 'key': key, 'ts': ts, 'wait': wait}
        logging.debug('Sending request to vk: server = {}, payload = {}'.format(server, payload))
        request = requests.get(server, params=payload)
        res = request.json()

        if 'failed' not in res:
            return res

        elif res['failed'] == 1:
            self.ts = res['ts']
            logging.warning('VK returned lp response with "failed" == 1, updated self.ts value')
            return self.long_poll(self.server, self.key, self.ts)
        elif res['failed'] in [2, 3]:
            self.key, self.server, self.ts = self.get_long_poll_server()
            logging.warning('VK returned lp response with "failed" == 2 or 3, updated Long Poll server')
            return self.long_poll(self.server, self.key, self.ts)
        else:
            raise Exception('VK returned lp response with unexpected "failed" value. Response: {}'.format(res))


def strip_push(text: str, group_id):
    return re.sub(r'\s*\[club' + str(group_id) + '\|.*?\]\s*', ' ', text).strip()
