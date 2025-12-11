import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import numpy as np

class TurtleBot:
    def __init__(self):
        rospy.init_node('turtle_controller', anonymous=True)
        self.velocity_publish = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) #we'll publish out the desired velocity to turtle1/cmd_vel
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose') #we'll subscribe to the topic that publishes the turtle's position
        
        self.pose = Pose()
        self.rate = rospy.Rate(10)
        
    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        
    def distance(self, target_pose):
        return np.sqrt((target_pose.x - self.pose.x)^2 + (target_pose.y - self.pose.y)^2)
    
    def vel(self, target_pose, const=1.5):
        return const * self.distance(target_pose)
    
    def turn_angle(self, target_pose):
        return np.arctan2()
    
    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        # Get the input from the user.
        goal_pose.x = float(input("Set your x goal: "))
        goal_pose.y = float(input("Set your y goal: "))

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = input("Set your tolerance: ")

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance: #until we reach the target
            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass