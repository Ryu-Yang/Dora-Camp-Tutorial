from dora import Node
import pyarrow as pa
from enum import Enum
import time

PID_X = 0.0004
PID_Y = -0.0003

class Action(Enum):
    FORWARD = ("arm forward",   "movec", [0.02, 0, 0, 0, 0, 0, 0.1])
    BACK    = ("arm backward",  "movec", [-0.02, 0, 0, 0, 0, 0, 0.1])
    LEFT    = ("arm left",      "movec", [0, -0.02, 0, 0, 0, 0, 0.1])
    RIGHT   = ("arm right",     "movec", [0, 0.02, 0, 0, 0, 0, 0.1])
    UP      = ("arm up",        "movec", [0, 0, -0.02, 0, 0, 0, 0.1])
    DOWN    = ("arm down",      "movec", [0, 0, 0.02, 0, 0, 0, 0.1])
    # CLOSE   = ("claw close",    "claw", [0])
    # OPEN    = ("claw open",     "claw", [100])
    SAVE    = ("save",          "save", [0])
    CLEAR   = ("clear",         "clear", [0])
    BEGIN   = ("begin",         "begin", [0])
    STOP    = ("stop",          "stop", [0])
    GOTO    = ("goto",          "goto", [0])

claw_state = 1

node = Node()

for event in node:
    if event["type"] == "INPUT":
        event_id = event["id"]
        if event_id == "key-keyboard" or event_id == "key-qwenvl":
            text = event["value"][0].as_py()
            text = text.replace(".", "")
            text = text.replace(".", "")

            for action in Action:
                if action.value[0] in text:
                    node.send_output(action.value[1], pa.array(action.value[2]))
                    print(f"""recieved:{action.value[0]}""")

            if "claw close" in text:
                if claw_state == 1:
                    claw_state = 0
                    DOWN = ("arm down", "movec", )
                    node.send_output("movec", pa.array([0, 0, 0.06, 0, 0, 0, 0.1]))
                    time.sleep(2)
                    node.send_output("claw", pa.array([0]))
                    time.sleep(2)
                    node.send_output("movec", pa.array([0, 0, -0.06, 0, 0, 0, 0.1]))
                    time.sleep(1)
            if "claw open" in text:
                claw_state = 1
                node.send_output("claw", pa.array([100]))

        if event["id"] == "error":
            [error_x, error_y] =  event["value"].tolist()
            move_error = [
                PID_Y*error_y,
                PID_X*error_x,
                0,
                0,
                0,
                0,
                0
            ]
            print(f"""move_error:{move_error}""")
            node.send_output("movec", pa.array(move_error))