#!/usr/bin/env python3

import os
import sys

import rospy
from std_msgs.msg import String, Int64
from game_ros.msg import user_msg   # custom message

# --- Add ../game_src to Python path so we can import game.py ---
this_dir = os.path.dirname(os.path.abspath(__file__))
game_src_path = os.path.join(this_dir, "..", "game_src")
sys.path.insert(0, game_src_path)

from game import Game   # uses Game class defined in game.py


class GameNode:
    def __init__(self):
        rospy.init_node("game_node")

        # Subscribers
        self.user_sub = rospy.Subscriber("user_information", user_msg,
                                         self.user_callback)
        self.control_sub = rospy.Subscriber("keyboard_control", String,
                                            self.control_callback)

        # Publisher for the final score
        self.result_pub = rospy.Publisher("result_information", Int64,
                                          queue_size=10)

        # Internal state
        self.player_info = None
        self.last_command = None
        self.phase = "WELCOME"   # WELCOME -> GAME -> FINAL

        # Snake game instance
        self.game = Game()

        rospy.loginfo("GAME_NODE: started.")

    def user_callback(self, msg):
        self.player_info = msg
        rospy.loginfo(f"GAME_NODE: got user info for {msg.username}")

    def control_callback(self, msg):
        self.last_command = msg.data  # "UP", "DOWN", ...

    # -------- Phases ----------

    def welcome_phase(self):
        if self.player_info is not None:
            print(f"\nWelcome, {self.player_info.name} (@{self.player_info.username})!")
            rospy.loginfo("GAME_NODE: switching to GAME phase.")
            self.phase = "GAME"

    def game_phase(self):
        # Pass command to the game, if we received one
        if self.last_command is not None:
            self.game.handle_command(self.last_command)
            self.last_command = None

        # Advance Snake game and draw frame
        self.game.update()
        self.game.draw()

        # If game finished, move to FINAL phase
        if self.game.is_over():
            rospy.loginfo("GAME_NODE: game over -> FINAL phase.")
            self.phase = "FINAL"

    def final_phase(self):
        score = self.game.get_score()
        msg = Int64()
        msg.data = score
        self.result_pub.publish(msg)
        rospy.loginfo(f"GAME_NODE: published final score {score}")
        rospy.signal_shutdown("Game finished")

    def run(self):
        rate = rospy.Rate(30)  # 30 Hz loop
        while not rospy.is_shutdown():
            if self.phase == "WELCOME":
                self.welcome_phase()
            elif self.phase == "GAME":
                self.game_phase()
            elif self.phase == "FINAL":
                self.final_phase()

            rate.sleep()


if __name__ == "__main__":
    node = GameNode()
    node.run()

