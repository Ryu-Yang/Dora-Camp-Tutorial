from pynput import keyboard
from pynput.keyboard import Events
import pyarrow as pa
from dora import Node
import time

node = Node()

with keyboard.Events() as events:
    while True:
        event = events.get(1.0)
        if event is not None and isinstance(event, Events.Press):
            if hasattr(event.key, "char"):
                if event.key.char == "p":
                    break
                if event.key.char == "z":
                    while True:
                        node.send_output("char", pa.array(["b"]))
                        time.sleep(5)
                if event.key.char is not None:
                    node.send_output("char", pa.array([event.key.char]))
