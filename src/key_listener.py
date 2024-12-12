from pynput import keyboard
from pynput.keyboard import Events
import pyarrow as pa
from dora import Node
import time


node = Node()


def on_press(key):
    try:
        if hasattr(key, "char"):
            if key.char is not None:
                node.send_output("press", pa.array([key.char]))
    except AttributeError:
        pass

def on_release(key):
    try:
        if hasattr(key, "char"):
            if key.char is not None:
                node.send_output("release", pa.array([key.char]))
    except AttributeError:
        pass


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# with keyboard.Events() as events:
#     while True:
#         event = events.get(1.0)
#         if event is not None and isinstance(event, Events.Press):
#             if hasattr(event.key, "char"):
#                 # if event.key.char == '\x1b':
#                 #     break
#                 # if event.key.char == "z":
#                 #     while True:
#                 #         node.send_output("char", pa.array(["b"]))
#                 #         time.sleep(5)
#                 if event.key.char is not None:
#                     node.send_output("char", pa.array([event.key.char]))


