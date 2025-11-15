#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

class ControlNode:
    def __init__(self):
        self.pub = rospy.Publisher("keyboard_control", String, queue_size=10)
        rospy.loginfo("CONTROL_NODE started. Use UP/DOWN/LEFT/RIGHT or QUIT.")
        self.run()

    def run(self):
        while not rospy.is_shutdown():
            cmd = input("Movement (UP/DOWN/LEFT/RIGHT or QUIT): ").strip().upper()
            if cmd == "":
                continue

            msg = String()
            msg.data = cmd
            self.pub.publish(msg)
            rospy.loginfo(f"Published: {cmd}")

            if cmd == "QUIT":
                break

if __name__ == "__main__":
    rospy.init_node("control_node")
    ControlNode()

