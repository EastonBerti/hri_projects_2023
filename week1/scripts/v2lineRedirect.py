#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
speed = 1.0
ASpeed = 1
PI = 3.1415926535897
angular_speed = ASpeed*360*PI/360
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
vel_msg = Twist() 
leftLaser = 10.0
rightLaser = 10.0
def callback(data):
	x = 0
	rangerDan = data.ranges
	global speed
	global angular_speed
	global leftLaser
	global rightLaser

	for i in rangerDan:
		if x >= 341 and x < 491: 
			if rightLaser < i:
				rightLaser = i

		if x >= 491 and x <= 591:
			speed = 0.2 + i/10.0
			vel_msg.linear.x = abs(speed)
			pub.publish(vel_msg)
			midLaser = i
			if i < 2.5:
				if rightLaser >= leftLaser:
					vel_msg.angular.z = -abs(angular_speed)
					pub.publish(vel_msg)
				else:
					vel_msg.angular.z = abs(angular_speed)
					pub.publish(vel_msg)
			else:
				vel_msg.angular.z = 0
				pub.publish(vel_msg)
				
		if x <= 741 and x > 591: 
			if leftLaser < i:
				leftLaser = i
		
		else:
			dumpelse = 0
		x = x + 1


def move():    
	# Starts a new node
	rospy.init_node('robot_cleaner', anonymous=True)
	rospy.Subscriber("/base_scan", LaserScan, callback)
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0    
	
	while not rospy.is_shutdown():
		spinvar = 2
	rospy.spin()
if __name__ == '__main__':
	try:
		#Testing our function
		move()
	except rospy.ROSInterruptException: pass