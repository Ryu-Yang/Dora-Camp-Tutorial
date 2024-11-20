# import
import numpy as np
from dora import Node
import json
import os
import time
from robotic_arm_package.robotic_arm import *
import sys

# define
SPEED = 50
SAVED_POSE_PATH = "./pose_library.json"
ROBOT_IP = os.getenv("ROBOT_IP", "192.168.1.18")
MIN_Z = float(os.getenv("MIN_Z", "0.0"))

assert ROBOT_IP is not None, "ROBOT_IP environment variable must be set"


# function
def load_json_file(file_path):
    """Load JSON file and return the dictionary."""
    with open(file_path, "r") as file:
        data = json.load(file)
        return data

def save_json_file(file_path, data):
    """Save the dictionary back to the JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# main
robot = Arm(72, ROBOT_IP)  # 创建实例
robot.Set_Tool_Voltage(3)
robot.Set_Modbus_Mode(1, 115200, 2, 2)

joint_d = [0, 45, 0, -90, 0, 45, 0]
robot.Movej_Cmd(joint_d, SPEED)
time.sleep(2)

data = robot.Get_Current_Arm_State()  # 获取机械臂运动数据
[x, y, z, rx, ry, rz] = list(data[2])  # 位置position
joint_angle= data[1]  # 当前的关节angle

logger_.info(
    f"Cartesian Pose: x={x}, y={y}, z={z}, rx={rx}, ry={ry}, rz={rz}"
)
logger_.info(f"joint_angle: {joint_angle}")

node = Node()
pose_library = load_json_file(SAVED_POSE_PATH)
logger_.info(f"pose_library: {pose_library}")

for event in node:
    if event["type"] == "INPUT":

        if event["id"] == "movec":
            [dx, dy, dz, drx, dry, drz, t] = event["value"].tolist()

            cartesian_pose = {
                "x": x + dx,
                "y": y + dy,
                "z": z + dz,
                "rx": rx + drx,
                "ry": ry + dry,
                "rz": rz + drz,
            } 

            x=x + dx
            y=y + dy
            z=z + dz
            rx=rx + drx
            ry=ry + dry
            rz=rz + drz

            cart_pose = [
                cartesian_pose[key] for key in ["x", "y", "z", "rx", "ry", "rz"]
            ]
            robot.Movel_Cmd(cart_pose, SPEED, block=False)

        elif event["id"] == "claw":
            [claw] = event["value"].tolist()
            robot.Write_Single_Register(1, 40000, claw, 1, 1)
        
        elif event["id"] == "save":
            id = pose_library["num"]
            robot.Move_Stop_Cmd()
            data = robot.Get_Current_Arm_State()
            [x, y, z, rx, ry, rz] = list(data[2])
            joint_angle = data[1]
            tag, claw = robot.Get_Read_Holding_Registers(1, 40000, 1)
            pose_library["pose"][id] = list(joint_angle)
            pose_library["claw"][id] = claw
            pose_library["num"] = pose_library["num"] + 1
        
        elif event["id"] == "clear":
            pose_library["num"] = 0
            pose_library["pose"].clear()
            pose_library["claw"].clear()

        elif event["id"] == "begin":
            robot.Move_Stop_Cmd()
            for i in range(pose_library["num"]):
                retrieved_pose = pose_library["pose"].get(i)
                retrieved_claw = pose_library["claw"].get(i)
                if retrieved_pose is not None:
                    joint_angle = retrieved_pose
                    robot.Movej_Cmd(joint_angle, SPEED, block=True)
                    robot.Write_Single_Register(1, 40000, retrieved_claw, 1, 1)
                    time.sleep(1)
                    data = robot.Get_Current_Arm_State()
                    [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
                    joint_angle = data[1]  # 当前的关节位置
        
        elif event["id"] == "stop":
            robot.Move_Stop_Cmd()
            data = robot.Get_Current_Arm_State()
            [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
            joint_angle = data[1]  # 当前的关节位置

        elif event["id"] == "goto":
            name = event["value"][0].as_py()
            robot.Move_Stop_Cmd()
            retrieved_pose = pose_library["pose"].get(name)
            retrieved_claw = pose_library["claw"].get(name)
            if retrieved_pose is not None:
                joint_angle = retrieved_pose
                robot.Movej_Cmd(joint_angle, SPEED, block=False)
                data = robot.Get_Current_Arm_State()
                [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
                joint_angle = data[1]  # 当前的关节位置

        save_json_file(SAVED_POSE_PATH, pose_library)
