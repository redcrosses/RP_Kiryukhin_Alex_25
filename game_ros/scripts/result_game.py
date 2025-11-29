#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int64
from game_ros.msg import user_msg

class ResultGameNode:
    def __init__(self):
        rospy.init_node('result_game')

        self.user_info = None
        self.score = None

        self.user_sub = rospy.Subscriber('user_information', user_msg,
                                         self.user_callback)
        self.result_sub = rospy.Subscriber('result_information', Int64,
                                           self.result_callback)

        rospy.loginfo("RESULT_GAME: waiting for user info and score...")

    def user_callback(self, msg):
        self.user_info = msg
        rospy.loginfo(f"RESULT_GAME: got user info for {msg.username}")
        self.maybe_print_result()

    def result_callback(self, msg):
        self.score = msg.data
        rospy.loginfo(f"RESULT_GAME: got score {self.score}")
        self.maybe_print_result()

    def maybe_print_result(self):
        if self.user_info is not None and self.score is not None:
            print(f"\nGAME OVER! User '{self.user_info.username}' scored {self.score} points.")
            rospy.loginfo("RESULT_GAME: printed result.")

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = ResultGameNode()
    node.run()
