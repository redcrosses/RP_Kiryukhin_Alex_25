#!/usr/bin/env python3
import rospy
from std_msgs.msg import String, Int64
from game_ros.msg import user_msg

class GameNode:
    def __init__(self):
        rospy.loginfo("GAME_NODE started.")

        self.user_info = None
        self.score = 0
        self.game_active = False

        rospy.Subscriber("user_information", user_msg, self.user_callback)
        rospy.Subscriber("keyboard_control", String, self.keyboard_callback)

        self.result_pub = rospy.Publisher("result_information", Int64, queue_size=10)

    def user_callback(self, msg):
        self.user_info = msg
        rospy.loginfo(f"Welcome {msg.name} (@{msg.username}), age {msg.age}")
        self.phase_welcome()
        self.phase_game()
        self.phase_final()

    def keyboard_callback(self, msg):
        if not self.game_active:
            return

        move = msg.data.upper()
        rospy.loginfo(f"Movement received: {move}")

        if move in ["UP", "DOWN", "LEFT", "RIGHT"]:
            self.score += 1

        if move == "QUIT":
            self.game_active = False

    def phase_welcome(self):
        rospy.loginfo("Welcome phase started.")
        rospy.sleep(1.0)

    def phase_game(self):
        rospy.loginfo("Game phase started.")
        self.game_active = True
        start = rospy.Time.now()

        rate = rospy.Rate(10)
        while not rospy.is_shutdown() and self.game_active:
            if (rospy.Time.now() - start).to_sec() > 30:
                rospy.loginfo("Time limit reached.")
                self.game_active = False
            rate.sleep()

        rospy.loginfo(f"Game ended. Score = {self.score}")

    def phase_final(self):
        rospy.loginfo("Final phase started. Publishing score...")
        msg = Int64()
        msg.data = self.score
        self.result_pub.publish(msg)

if __name__ == "__main__":
    rospy.init_node("game_node")
    GameNode()
    rospy.spin()
