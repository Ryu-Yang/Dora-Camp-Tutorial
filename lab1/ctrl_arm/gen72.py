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


    








# def main():
#     # Load the JSON file
#     pose_library = load_json_file(SAVED_POSE_PATH)
#     node = Node()
#     recording = False
#     teaching = False
#     recording_name = None
#     data = robot.Get_Current_Arm_State()  # 获取机械臂运动数据
#     [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
#     joint_position = data[1]  # 当前的关节位置
#     t = 0.15

#     for event in node:
#         if event["type"] == "INPUT":
#             # pylint: disable=fixme
#             # TODO: Remove this after https://github.com/dora-rs/dora/pull/652
#             while True:
#                 next_event = node.next(timeout=0.001)
#                 if next_event is not None and next_event["type"] == "INPUT":
#                     event = next_event
#                 else:
#                     break
#             event_id = event["id"]
#             if event_id == "claw":
#                 [claw] = event["value"].tolist()
#                 robot.Write_Single_Register(1, 40000, claw, 1, 1)
#             elif event_id == "movec":
#                 if teaching:
#                     continue
#                 [dx, dy, dz, drx, dry, drz, t] = event["value"].tolist()
#                 if z < MIN_Z and dz < 0.0:
#                     print("z is less than MIN_Z", flush=True)
#                     dz = 0

#                 cartesian_pose = {
#                     "x": x + dx,
#                     "y": y + dy,
#                     "z": z + dz,
#                     "rx": rx + drx,
#                     "ry": ry + dry,
#                     "rz": rz + drz,
#                 }  # 目标位姿笛卡尔数据

#                 cart_pose = [
#                     cartesian_pose[key] for key in ["x", "y", "z", "rx", "ry", "rz"]
#                 ]
#                 # 使用 logger_.info() 替换 print() 来打印 cart_pose 列表的内容
#                 #t = 0.25  # 运动时间 (s)。 当 t > 0 时，参数速度 v 和加速度 a 无效
#                 try:
#                     joint_position_temp = robot.Algo_Inverse_Kinematics(
#                         joint_position, cart_pose, 1
#                     )  # 反解，将笛卡尔位置和姿态转换成关节角度
#                     joint_position = joint_position_temp[1]
#                 except TypeError:
#                     print("could not compute inverse kinematics")
#                     continue
#                 [x, y, z, rx, ry, rz] = list(cart_pose)
#                 logger_.info(
#                     f"Cartesian Pose: x={x}, y={y}, z={z}, rx={rx}, ry={ry}, rz={rz}"
#                 )
#                 # joint_d=[0.0]*7
#                 joint_d = joint_position_temp[1]
#                 logger_.info(f"joint_d: {joint_d}")
#                 robot.Movej_Cmd(joint_d, 20)
#                 # 指定每个关节的速度、加速度，让机器人连续地进行伺服运动。
#                 # 直线运动 https://help.lebai.ltd/sdk/motion.html#%E7%9B%B4%E7%BA%BF%E8%BF%90%E5%8A%A8
#                 # p。关节位置
#                 # v。每个关节的速度 (rad/s)
#                 # a。每个关节的加速度 (rad/s2)
#                 # t。运动时间 (s)
#             elif event_id == "movej":
#                 if teaching:
#                     continue
#                 relative_joint_position = event["value"].to_numpy()
#                 joint_position = np.array(joint_position)
#                 joint_position += np.array(relative_joint_position[:7])
#                 cartesian_pose = robot.Algo_Forward_Kinematics(joint_position)  # 正解
#                 [x, y, z, rx, ry, rz] = list(cartesian_pose)
#                 t = 0.15  # 运动时间 (s)。 当 t > 0 时，参数速度 v 和加速度 a 无效
#                 robot.Movej_Cmd(joint_position, 20)
#                 # 直线运动 https://help.lebai.ltd/sdk/motion.html#%E7%9B%B4%E7%BA%BF%E8%BF%90%E5%8A%A8
#             elif event_id == "stop":
#                 robot.Move_Stop_Cmd()
#                 data = robot.Get_Current_Arm_State()
#                 [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
#                 joint_position = data[1]  # 当前的关节位置
#             elif event_id == "save":
#                 name = event["value"][0].as_py()
#                 robot.Move_Stop_Cmd()
#                 data = robot.Get_Current_Arm_State()
#                 [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
#                 joint_position = data[1]  # 当前的关节位置
#                 pose_library["pose"][name] = list(joint_position)
#             elif event_id == "go_to":
#                 if teaching:
#                     continue
#                 name = event["value"][0].as_py()
#                 robot.Move_Stop_Cmd()
#                 retrieved_pose = pose_library["pose"].get(name)
#                 if retrieved_pose is not None:
#                     joint_position = retrieved_pose
#                     t = 2
#                     robot.Movej_Cmd(joint_position, 20)
#                     # 直线运动 https://help.lebai.ltd/sdk/motion.html#%E7%9B%B4%E7%BA%BF%E8%BF%90%E5%8A%A8
#                     # lebai.wait_move()#等待运动完成，motion_id move_xxx 返回的 motion_id。可选，默认为0全部运动
#                     data = robot.Get_Current_Arm_State()
#                     [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
#                     joint_position = data[1]  # 当前的关节位置
#             elif event_id == "record":
#                 name = event["value"][0].as_py()
#                 recording = True

#                 recording_name = name
#                 pose_library["recording"][recording_name] = []
#                 start_time = time.time()
#                 data = robot.Get_Current_Arm_State()
#                 [x, y, z, rx, ry, rz] = list(data[2])  # 末端工具位置
#                 joint_position = data[1]  # 当前的关节位置
#             elif event_id == "cut":
#                 recording = False
#             elif event_id == "teach":
#                 if teaching:
#                     teaching = False
#                     continue
#                 robot.Start_Drag_Teach()  # 进入示教模式
#                 teaching = True
#             elif event_id == "end_teach":
#                 teaching = False
#                 robot.Stop_Drag_Teach()  # 退出示教模式
#             elif event_id == "play":
#                 name = event["value"][0].as_py()
#                 if name in pose_library["recording"]:
#                     for event in pose_library["recording"][name]:
#                         print(event, flush=True)
#                         robot.Movej_Cmd(joint_position, 20)
#                         event = node.next(timeout=event["duration"])
#                         if event is not None:
#                             print(event)
#                             if event["type"] == "INPUT" and event["id"] == "stop":
#                                 robot.Move_Stop_Cmd()
#                                 break

#             else:
#                 pass
#             if recording and (
#                 event_id == "movej" or event_id == "movec" or event_id == "go_to"
#             ):
#                 if len(pose_library["recording"][recording_name]) == 0:
#                     t = 2
#                 pose_library["recording"][recording_name] += [
#                     {
#                         "duration": time.time() - start_time,
#                         "joint_position": joint_position,
#                         "t": t * 2 if t == 0.1 else t,
#                     }
#                 ]
#                 start_time = time.time()

#         save_json_file(SAVED_POSE_PATH, pose_library)
