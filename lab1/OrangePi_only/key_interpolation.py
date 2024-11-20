from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "keyboard":
            char = event["value"][0].as_py()
            print(f"""Keyboard recieved: {char}""")
            if   char == "w":
                node.send_output("text", pa.array(["forward"]))
            elif char == "s":
                node.send_output("text", pa.array(["backward"]))
            elif char == "d":
                node.send_output("text", pa.array(["right"]))
            elif char == "a":
                node.send_output("text", pa.array(["left"]))
            elif char == "q":
                node.send_output("text", pa.array(["arm take"]))
            elif char == "e":
                node.send_output("text", pa.array(["arm put"]))
            elif char == "t":
                node.send_output("text", pa.array(["arm Xp"]))
            elif char == "g":
                node.send_output("text", pa.array(["arm Xn"]))
            elif char == "f":
                node.send_output("text", pa.array(["arm Yn"]))
            elif char == "h":
                node.send_output("text", pa.array(["arm Yp"]))
            elif char == "r":
                node.send_output("text", pa.array(["arm Zp"]))
            elif char == "y":
                node.send_output("text", pa.array(["arm Zn"]))
            elif char == "x":
                node.send_output("text", pa.array(["save"]))
            elif char == "c":
                node.send_output("text", pa.array(["clear"]))
            elif char == "b":
                node.send_output("text", pa.array(["begin"]))
            elif char == "n":
                node.send_output("text", pa.array(["stop"]))
            elif char == "m":
                node.send_output("text", pa.array(["goto"]))
