from dora import Node
import pyarrow as pa
from enum import Enum

class Action(Enum):
    Xp      = ("arm Xp", "movec", [0.01, 0, 0, 0, 0, 0, 0.1])
    Xn      = ("arm Xn", "movec", [-0.01, 0, 0, 0, 0, 0, 0.1])
    Yp      = ("arm Yp", "movec", [0, 0.01, 0, 0, 0, 0, 0.1])
    Yn      = ("arm Yn", "movec", [0, -0.01, 0, 0, 0, 0, 0.1])
    Zp      = ("arm Zp", "movec", [0, 0, 0.01, 0, 0, 0, 0.1])
    Zn      = ("arm Zn", "movec", [0, 0, -0.01, 0, 0, 0, 0.1])
    take    = ("arm take", "claw", [0])
    put     = ("arm put", "claw", [100])
    save    = ("save", "save", [0])
    clear   = ("clear", "clear", [0])
    begin   = ("begin", "begin", [0])
    stop    = ("stop", "stop", [0])
    goto    = ("goto", "goto", [0])

node = Node()

for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "text":
            text = event["value"][0].as_py()
            text = text.replace(".", "")
            text = text.replace(".", "")

            for action in Action:
                if action.value[0] in text:
                    node.send_output(action.value[1], pa.array(action.value[2]))
                    print(f"""recieved:{action.value[0]}""")
