# ROS Assignment – game_ros

This package is for the publisher/subscriber exercise from the Robot Programming class.  
It contains several ROS nodes that communicate using topics and a custom message.

## Package contents
- Custom message: `user_msg.msg`
- Nodes:
  - `info_user_node.py`
  - `game_node.py`
  - `control_node.py`
  - `result_node.py`

## What each node does
- **info_user_node** – asks for name, username, age and publishes them on `/user_information`.
- **game_node** – main logic of the game (welcome, game, final).  
  Subscribes to user info and keyboard input and publishes the score.
- **control_node** – reads movement commands (UP, DOWN, LEFT, RIGHT, QUIT) from the terminal and publishes them.
- **result_node** – receives the final score and user info and prints the result.

## Topics used
- `/user_information` (custom msg `user_msg`)
- `/keyboard_control` (`std_msgs/String`)
- `/result_information` (`std_msgs/Int64`)

## How to build
Copy the game_ros folder into your catkin workspace. Then, from your workspace:
```
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

## How to run (open each in its own terminal)
1. `roscore`
2. `rosrun game_ros game_node.py`
3. `rosrun game_ros result_node.py`
4. `rosrun game_ros info_user_node.py`
5. `rosrun game_ros control_node.py`

After filling in the required info(age, name etc), you can send commands (UP, DOWN, LEFT, RIGHT, QUIT) in the control node terminal.

That's it.

## How to run (using the launch files)
1. in one terminal, run roslaunch game_ros game.launch
2. in another terminal, run roslaunch game_ros control.launch
3. in the third terminal, run roslaunch game_ros result.launch

Fill in your user information in the first terminal and press any key to start the game. In the second terminal, you can send commands (UP, DOWN, LEFT, RIGHT) and in the third terminal you can see the saved game results.