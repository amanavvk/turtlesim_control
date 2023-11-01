# turtlesim_control
This repository simulates the turtlesim package, subjecting them to diverse conditions, including scenarios with intermittent and noisy communication. Additionally, it incorporates a planning component enabling a slower follower robot to synchronize its movements with a faster leader robot. For further details, you can access the PDF report by following [this link]

## requirements:

1. ROS Noetic
2. Ubuntu 18.04

## GOALS
### Goal 1: Navigate the turtlebot from a random location to an input location without overshooting and using PID control.
To achieve this goal, I defined specific constants for proportional, derivative, and integral gains. These constants were used to calculate errors (referred to as p, d, and i) within iterative loops, and the robot's velocity was continuously updated and published. This process continued until the robot's self-position closely aligned with the target location, with a predefined tolerance. By adjusting this tolerance value, which is currently set at 0.5, I was able to enhance the precision of goal achievement. In this context, the linear velocity parameter was determined as the distance between the robot's current position and the goal position. Alternatively, it could be computed as the difference between the current and goal coordinates, accommodating both forward and reverse velocities. However, I resolved this issue by appropriately setting angular velocities.
This entire process was orchestrated using the 'turtle_precise_navigation.launch' launch file.
 ![goal_1_gif](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_1.gif)
 ![goal_1](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_1.png)
here is the full [video](https://drive.google.com/file/d/13M8REZk7_yfYwVU0FaYQHi5nOvwr_e6j/view)


### Goal 2: Implement maximum accelerations and form a grid path
To constrain accelerations, a function "step_vel" has been employed. Within this approach, the desired velocity is transmitted and is progressively incremented in discrete steps. Prior to the publication of this modified velocity, a thorough assessment of the step's value is conducted.
The maximum acceleration limits are set and can be adjusted as needed. In each stage of velocity increment, the corresponding time interval, denoted as delta(time), is recorded. If the ratio of the velocity step to the delta(time) exceeds the maximum permissible value, the step size is reset to the maximum allowable value for that specific delta(time).
![goal_2](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_2_1.gif)

for Grid making process:
The grid task can be though as discrete sections.
1. From any random location, go to the starting position in fastest way possible.
2. Thereafter, grid points are defined which have to be followed. Hence, fastest way
would give a curvature and not follow lines. Thus, grid corners are defined.
3. However, at the end of a corner, the orientation of the turtle is perpendicular to
next line that has to be followed. Directly commanding to go the next corner would
again give a curvature. (Note: The lines are given importance, if that wasn’t the case,
subsequent calls to goal_reach(target) would suffice.)
4. To avoid curvature at the end, a rotate() function has been defined. This takes in
an angle and rotates it with proportional control.
5. Finally, the grid function is defined. Grid_corners contain x,y coordinates, as well
as angles to be rotated at the end of traversal. Go_to_goal() is then called.
![goal_2_gif](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_2_2.gif)

### Goal 3: Take user input radius and velocity limit to form circular path with the turtlebot
The `circles()` function initiates user input for radius and velocity, leading to the computation of angular velocity. Once these values are established, the `step_vel()` function is employed to incrementally increase the turtle's velocity. Upon launch, a time variable is initialized, and every 5 seconds, this variable triggers the publication of two poses: `rt_real_pose`, representing the precise turtle pose, and `rt_noisy_pose`, which introduces random Gaussian noise. 
![goal_3_gif](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_3.gif)

### Goal 4:Chase turtle fast
Initially, the `turtlesim_node` is initiated with a single turtle.
Subsequently, the circling motion of this 'Robber Turtle' is initiated using the circle function from Goal 3.
To introduce another turtle, the `turtlespawn` node is employed, which involves a 10-second delay. Following this delay, it invokes the 'spawn' service, assigning random values for the creation of another turtle, referred to as 'turtle2'. It's worth noting that the service could also return the name, but considering that only one of the launch files is typically executed at any given time, there shouldn't be any naming conflicts.
The increased speed enables the 'PT' (Pursuer Turtle) to rapidly reach the last known location of 'RT' (Robber Turtle). However, the difference in their speeds determines the distance between them when the next 'rt_real_pose' update is received. If 'PT' arrives within 5 seconds, it will pause at the last known location of 'RT'. Several scenarios are possible in this situation. 
![goal_4_gif](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_4_1.gif)

### Goal 5:Chase turtle slow
In the preceding example, the discrepancy in velocities playe
d a crucial role in the pursuit dynamics. With PT moving at a higher speed, it consistently gained ground on RT, albeit in incremental increments. This happened because PT swiftly reached its most recent location, and RT, with its slower pace, lagged behind. Consequently, the subsequent position update further reduced the separation between them, instilling confidence in their eventual convergence.
![goal_5_gif](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_5_2.gif)

### Goal 6:Chase turtle noisy
In the pursuit of our objective, when the Real-Time (RT) system introduces pose data with Gaussian noise, it introduces a level of complexity to the planning process. The extent of uncertainty in successfully reaching the target is contingent on both the mean and standard deviation of the Gaussian noise. Opting for higher standard deviation values while keeping the Planning-Time (PT) half as fast as RT can result in PT being unable to keep up with RT. Even in the presence of Gaussian noise and a specified threshold of 3 units, PT can approach RT closely enough to conclude the pursuit. The rapid fluctuations introduced by random Gaussian noise may potentially destabilize PT. In a provided video example, PT managed to approach RT when the standard deviation was set to 1, eventually reaching proximity and ending the pursuit.
![goal_6_gif](https://github.com/amanavvk/turtlesim_control/blob/master/images%20and%20gifs/goal_6_1.gif)
