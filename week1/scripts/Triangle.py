#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def move():
	# Starts a new node
	rospy.init_node('robot_cleaner', anonymous=True)
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()
	PI = 3.1415926535897
	#Receiveing the user's input\
	speed = 1
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	angular_speed = speed*45*PI/360
	while not rospy.is_shutdown():
		
		vel_msg.linear.x = abs(speed)
		for i in range(75000):
			pub.publish(vel_msg)
		vel_msg.linear.x = 0
		pub.publish(vel_msg)
		vel_msg.angular.z = abs(angular_speed)
		#Loop to move the turtle in an specified distance
		for i in range(240000):
			pub.publish(vel_msg)
		vel_msg.angular.z = 0
		pub.publish(vel_msg)

		
		

if __name__ == '__main__':
	try:
		#Testing our function
		move()
	except rospy.ROSInterruptException: pass