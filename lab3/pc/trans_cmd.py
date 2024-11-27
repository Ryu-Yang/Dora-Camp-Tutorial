from dora import Node
import pyarrow as pa
from enum import Enum


class Action(Enum):
    FORWARD = ("arm forward",   "movec", [0.02, 0, 0, 0, 0, 0, 0.1])
    BACK    = ("arm backward",  "movec", [-0.02, 0, 0, 0, 0, 0, 0.1])
    LEFT    = ("arm left",      "movec", [0, -0.02, 0, 0, 0, 0, 0.1])
    RIGHT   = ("arm right",     "movec", [0, 0.02, 0, 0, 0, 0, 0.1])
    UP      = ("arm up",        "movec", [0, 0, -0.02, 0, 0, 0, 0.1])
    DOWN    = ("arm down",      "movec", [0, 0, 0.02, 0, 0, 0, 0.1])
    CLOSE   = ("claw close",    "claw", [0])
    OPEN    = ("claw open",     "claw", [100])
    SAVE    = ("save",          "save", [0])
    CLEAR   = ("clear",         "clear", [0])
    BEGIN   = ("begin",         "begin", [0])
    STOP    = ("stop",          "stop", [0])
    GOTO    = ("goto",          "goto", [0])


node = Node()

for event in node:
    if event["type"] == "INPUT":
        text = event["value"][0].as_py()
        text = text.replace(".", "")
        text = text.replace(".", "")

        for action in Action:
            if action.value[0] in text:
                node.send_output(action.value[1], pa.array(action.value[2]))
                print(f"""recieved:{action.value[0]}""")
