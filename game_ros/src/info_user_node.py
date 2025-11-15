#!/usr/bin/env python3
import rospy
from game_ros.msg import user_msg    # custom message

class InfoUserNode:
    def __init__(self):
        self.pub = rospy.Publisher("user_information", user_msg, queue_size=10)
        rospy.loginfo("INFO_USER ready. Asking for player info...")
        rospy.sleep(1.0)
        self.run()

    def run(self):
        name = input("Enter your name: ")
        username = input("Enter your username: ")

        while True:
            try:
                age = int(input("Enter your age: "))
                break
            except ValueError:
                print("Age must be an integer!")

        msg = user_msg()
        msg.name = name
        msg.username = username
        msg.age = age

        rospy.loginfo(f"Publishing user info: {msg}")
        self.pub.publish(msg)

if __name__ == "__main__":
    rospy.init_node("info_user")
    InfoUserNode()
    rospy.spin()
