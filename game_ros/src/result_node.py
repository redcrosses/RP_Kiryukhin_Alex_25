#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int64
from game_ros.msg import user_msg

class ResultNode:
    def __init__(self):
        self.user_info = None
        self.score = None

        rospy.Subscriber("user_information", user_msg, self.user_callback)
        rospy.Subscriber("result_information", Int64, self.score_callback)

        rospy.loginfo("RESULT_NODE started.")

    def user_callback(self, msg):
        self.user_info = msg
        self.check_done()

    def score_callback(self, msg):
        self.score = msg.data
        self.check_done()

    def check_done(self):
        if self.user_info is not None and self.score is not None:
            rospy.loginfo(
                f"FINAL RESULT: @{self.user_info.username} ({self.user_info.name}, age {self.user_info.age}) scored {self.score} points!"
            )

if __name__ == "__main__":
    rospy.init_node("result_node")
    ResultNode()
    rospy.spin()

