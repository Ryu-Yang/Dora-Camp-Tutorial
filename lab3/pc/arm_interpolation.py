from dora import Node
import pyarrow as pa
from enum import Enum
import time
node = Node()


class Action(Enum):
    """
    Action abstraction
    """

    FORWARD = ("arm forward", "movec", [0.02, 0, 0, 0, 0, 0, 0.1])
    BACK = ("arm backward", "movec", [-0.02, 0, 0, 0, 0, 0, 0.1])
    LEFT = ("arm left", "movec", [0, 0.02, 0, 0, 0, 0, 0.1])
    RIGHT = ("arm right", "movec", [0, -0.02, 0, 0, 0, 0, 0.1])
    UP = ("arm up", "movec", [0, 0, 0.02, 0, 0, 0, 0.1])
    DOWN = ("arm down", "movec", [0, 0, -0.02, 0, 0, 0, 0.1])
    CLOSE = ("close", "claw", [0])
    OPEN = ("open", "claw", [100])
    # STOP = ("stop", "stop", [])
    SAVE = ("save", "save", [])
    GO_TO = ("go", "go_to", [])
    # END_TEACH = ("end of teach", "end_teach", [])
    # TEACH = ("teach", "teach", [])



for event in node:
    if event["type"] == "INPUT":
        text = event["value"][0].as_py().lower()
        text = text.replace(".", "")
        text = text.replace(".", "")

        if "save" in text:
            node.send_output("save", pa.array([text.replace("save ", "")]))
        elif "go" in text:
            node.send_output("go_to", pa.array([text.replace("go ", "")]))
        elif "go to " in text:
            node.send_output("go_to", pa.array([text.replace("go to ", "")]))
        else:
            for action in Action:
                if action.value[0] in text:
                    node.send_output(action.value[1], pa.array(action.value[2]))
