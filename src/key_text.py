from dora import Node
import pyarrow as pa


recorder_flag = False

node = Node()

for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "key-press":
            char = event["value"][0].as_py()
            print(f"""key-press recieved: {char}""")

            if char == "p":
                recorder_flag = not recorder_flag
                node.send_output("recorder_flag", pa.array([recorder_flag]))
            elif char == "w":
                node.send_output("text", pa.array(["forward"]))
            elif char == "s":
                node.send_output("text", pa.array(["backward"]))
            elif char == "d":
                node.send_output("text", pa.array(["right"]))
            elif char == "a":
                node.send_output("text", pa.array(["left"]))
            elif char == "q":
                node.send_output("text", pa.array(["claw close"]))
            elif char == "e":
                node.send_output("text", pa.array(["claw open"]))
            elif char == "t":
                node.send_output("text", pa.array(["arm forward"]))
            elif char == "g":
                node.send_output("text", pa.array(["arm backward"]))
            elif char == "f":
                node.send_output("text", pa.array(["arm left"]))
            elif char == "h":
                node.send_output("text", pa.array(["arm right"]))
            elif char == "r":
                node.send_output("text", pa.array(["arm up"]))
            elif char == "y":
                node.send_output("text", pa.array(["arm down"]))
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

            if recorder_flag:
                if char == "z":
                    node.send_output("truth", pa.array(["wait"]))
                elif char == "w":
                    node.send_output("truth", pa.array(["forward"]))
                elif char == "s":
                    node.send_output("truth", pa.array(["backward"]))
                elif char == "d":
                    node.send_output("truth", pa.array(["right"]))
                elif char == "a":
                    node.send_output("truth", pa.array(["left"]))
                elif char == "q":
                    node.send_output("truth", pa.array(["claw close"]))
                elif char == "e":
                    node.send_output("truth", pa.array(["claw open"]))
                elif char == "t":
                    node.send_output("truth", pa.array(["arm forward"]))
                elif char == "g":
                    node.send_output("truth", pa.array(["arm backward"]))
                elif char == "f":
                    node.send_output("truth", pa.array(["arm left"]))
                elif char == "h":
                    node.send_output("truth", pa.array(["arm right"]))
                elif char == "r":
                    node.send_output("truth", pa.array(["arm up"]))
                elif char == "y":
                    node.send_output("truth", pa.array(["arm down"]))

        if event["id"] == "key-release":
            char = event["value"][0].as_py()
            if char == "t":
                node.send_output("text", pa.array(["arm stop"]))
            elif char == "g":
                node.send_output("text", pa.array(["arm stop"]))
            elif char == "f":
                node.send_output("text", pa.array(["arm stop"]))
            elif char == "h":
                node.send_output("text", pa.array(["arm stop"]))
            elif char == "r":
                node.send_output("text", pa.array(["arm stop"]))
            elif char == "y":
                node.send_output("text", pa.array(["arm stop"]))