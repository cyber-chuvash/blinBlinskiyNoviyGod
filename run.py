import threading

from blin import blin
from blin.longpoll import Receiver

r = Receiver()

timer = threading.Thread(target=blin.start_loop, daemon=True)
timer.start()
rec = threading.Thread(target=r.start_loop, daemon=True)
rec.start()

timer.join()

