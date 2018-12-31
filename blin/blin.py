import time
import logging

from blin.config import Config
from blin.database import Database
from blin.vk import API
from blin.numerals import get_seconds

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
    level=Config.log_level
)

#
# # datetime = Config.datetime
# datetime = time.time() + 12
# # checkpoints = (60, 30, 10, 5, 4, 3, 2, 1)
# # checkpoints = Config.checkpoints
# checkpoints = (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)


def start_loop():
    db = Database()
    for checkpoint in Config.checkpoints:

        sleeptime = Config.datetime - time.time() - checkpoint

        if sleeptime > 0:
            logging.info(f'Sleeping for {sleeptime} seconds')
            time.sleep(sleeptime)
        else:
            if checkpoint != Config.checkpoints[-1]:
                continue

        for chat in db.chats:
            API.messages.send(
                peer_id=chat,
                message=f'Блин блинский, до нового года {get_seconds(checkpoint)}',
                random_id=0
            )

    for chat in db.chats:
        API.messages.send(peer_id=chat, message=f'Блин блинский, до нового года 31536000 секунд', random_id=0)

