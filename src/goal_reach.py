#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import atan2, sqrt
import time
class turtle():
	def __init__(self):
		rospy.init_node('goal_navigation')
		self.position=Pose()
		self.vel_pub=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
		self.rate=rospy.Rate(10)                        
		self.pose_sub=rospy.Subscriber('/turtle1/pose',Pose,self.callback)
		
	def callback(self,data):#Update value of poses
		self.position=data
	
	def goal_reach(self):	
		goal=Pose()
		goal.x=input("Enter x coordinate of goal:")
		goal.y=input("Enter y coordinate of goal:")
		start_time=time.time()
		vel=Twist()
		Kp=1
		Kd=0.1
		Ki=0.0001
		dist_prev=sqrt((self.position.x-float(goal.x))**2+(self.position.y-float(goal.y))**2)
		e_sum=0           	#Initialise error summation terms for integral control
		steering_sum=0
		steering_prev=(atan2(float(goal.y) - self.position.y, float(goal.x) - self.position.x)-self.position.theta)
		while(True):
			e_sum=e_sum+dist_prev
			dist=sqrt((self.position.x-float(goal.x))**2+(self.position.y-float(goal.y))**2)
			dedt=dist-dist_prev	
			vel.linear.x=Kp*(dist)+Kd*dedt+Ki*e_sum	#PID Implementation
			steering=(atan2(float(goal.y) - self.position.y, float(goal.x)- self.position.x)-self.position.theta)   #Angle needed to turn
			dsteering=steering-steering_prev
			vel.angular.z=6*Kp*steering+Kd*dsteering+Ki*steering_sum	
			self.vel_pub.publish(vel)
			self.rate.sleep()
			dist_prev=dist
			steering_prev=steering
			steering_sum=steering_sum+steering_prev
			if(dist<0.5):
				stop_time=time.time()
				print("Reached goal")
				break
		print("Total time taken:",stop_time-start_time)
		




x=turtle()
while not rospy.is_shutdown():
	x.goal_reach()

		

