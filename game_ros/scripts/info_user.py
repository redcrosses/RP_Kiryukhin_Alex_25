#!/usr/bin/env python3
import rospy
from game_ros.msg import user_msg

class InfoUserNode:
    def __init__(self):
        rospy.init_node('info_user')
        self.pub = rospy.Publisher('user_information', user_msg, queue_size=10)

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

        rospy.loginfo("INFO_USER: Done. Waiting so other nodes can still receive it.")
        rospy.spin()

if __name__ == '__main__':
    node = InfoUserNode()
    node.run()
