#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import sys
import termios
import tty

class ControlNode:
    def __init__(self):
        rospy.init_node('control_node')
        self.pub = rospy.Publisher('keyboard_control', String, queue_size=10)
        rospy.loginfo("CONTROL_NODE: Use WASD to move, q to quit.")

    def getch(self):
        """Read a single character from terminal (no Enter needed)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        while not rospy.is_shutdown():
            key = self.getch()
            msg = String()

            if key == 'w':
                msg.data = "UP"
            elif key == 's':
                msg.data = "DOWN"
            elif key == 'a':
                msg.data = "LEFT"
            elif key == 'd':
                msg.data = "RIGHT"
            elif key == '1':
                msg.data = "1"
            elif key == '2':
                msg.data = "2"
            elif key == '3':
                msg.data = "3"
            elif key == 'q':
                rospy.loginfo("CONTROL_NODE: quit key pressed.")
                break
            else:
                continue  # ignore other keys

            rospy.loginfo(f"CONTROL_NODE: Publishing {msg.data}")
            self.pub.publish(msg)

if __name__ == '__main__':
    node = ControlNode()
    node.run()
