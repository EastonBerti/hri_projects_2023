#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from people_msgs.msg import PositionMeasurementArray
import copy
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster

global tf

speed = 1.0
ASpeed = 1
PI = 3.1415926535897
angular_speed = ASpeed*360*PI/360
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
vel_msg = Twist() 
leftLaser = 10.0
rightLaser = 10.0
corpDan = None

def callbackLaser(data):
	global corpDan
	corpDan = copy.deepcopy(data.ranges)

def callbackTracker(data):
	global tf
	person = data.people[0]
	tf = TransformStamped()
	tf.transform.translation.x = person.pos.x
	tf.transform.translation.y = person.pos.y
	tf.transform.translation.z = person.pos.z

	quat = Quaternion()
	quat.w = 1

	tf.transform.rotation = quat

	tf.header.frame_id = "odom"
	tf.header.stamp = rospy.Time().now()
	tf.child_frame_id = "person"
	#do math to figure angle to turn towards, their position minus mine to find array, 
	# angle of vector turn towards then go straight
	#google angle finding 

# def  tfpublish():


def move():    
	# Starts a new node
	global speed
	global angular_speed
	global leftLaser
	global rightLaser
	global corpDan
	global tf
	
	rospy.init_node('robot_cleaner', anonymous=True)
	rospy.Subscriber("/base_scan", LaserScan, callbackLaser)
	rospy.Subscriber("people_tracker_measurements", PositionMeasurementArray, callbackTracker)
	tfBroad = TransformBroadcaster()
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0    
	while corpDan == None:
		pass
	while not rospy.is_shutdown():
		try:
			tfBroad.sendTransform(tf)
		except NameError:
			continue
		# x=0
		# for i in corpDan:
		# #instert stalker program here, avoidance should take priority


		# #obstacle avoidance
		# 	if x >= 341 and x < 491: 
		# 		if rightLaser < i:
		# 			rightLaser = i

		# 	if x >= 491 and x <= 591:
		# 		speed = 0.2 + i/10.0
		# 		vel_msg.linear.x = abs(speed)
		# 		pub.publish(vel_msg)
		# 		midLaser = i
		# 		if i < 2.5:
		# 			if rightLaser >= leftLaser:
		# 				vel_msg.angular.z = -abs(angular_speed)
		# 				pub.publish(vel_msg)
		# 			else:
		# 				vel_msg.angular.z = abs(angular_speed)
		# 				pub.publish(vel_msg)
		# 		else:
		# 			vel_msg.angular.z = 0
		# 			pub.publish(vel_msg)
					
		# 	if x <= 741 and x > 591: 
		# 		if leftLaser < i:
		# 			leftLaser = i
			
		# 	else:
		# 		pass
		# 	x = x + 1

if __name__ == '__main__':
	try:
		#Testing our function
		move()
	except rospy.ROSInterruptException: pass