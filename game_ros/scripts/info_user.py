#!/usr/bin/env python3
import rospy
from game_ros.msg import user_msg
from game_ros.srv import SetGameDifficulty

class InfoUserNode:
    def __init__(self):
        rospy.init_node('info_user')
        self.pub = rospy.Publisher('user_information', user_msg, queue_size=10)
        self.serv = rospy.Service("difficulty", SetGameDifficulty, self.gameDifficulty)
        
    def run(self):
        rospy.loginfo("INFO_USER: Requesting user info...")

        name = input("Enter your full name: ")
        username = input("Enter your username: ")
        age = int(input("Enter your age: "))

        msg = user_msg()
        msg.name = name
        msg.username = username
        msg.age = age

        rospy.loginfo("INFO_USER: Publishing user information...")
        self.pub.publish(msg)
        rospy.set_param("user_name", name)
        
        rospy.loginfo("INFO_USER: Done. Waiting so other nodes can still receive it.")
        rospy.spin()
    def gameDifficulty(obj, req):
        phase = rospy.get_param("game_phase", default=False)
        if phase == "WELCOME":
            # print(type(req.difficulty))
            if req.difficulty in ["easy", "medium", "hard"]:
                rospy.set_param("difficulty", req.difficulty)
                return True
            else:
                return False
        
        else: return False
            
if __name__ == '__main__':
    node = InfoUserNode()
    node.run()
