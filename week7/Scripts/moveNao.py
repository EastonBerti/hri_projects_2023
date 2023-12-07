#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
import time
jointPain = None

def moveNao():
	rospy.init_node('nao_movement', anonymous=True)
	pub = rospy.Publisher('joint_states', JointState, queue_size=10)
	rate = rospy.Rate(10)
	mainState = JointState()
	start = 1.15
	finish = -1.5
	splits = 20
	while not rospy.is_shutdown():
		mainState.header.stamp = rospy.get_rostime()
		mainState.header.frame_id = "Torso"
		mainState.name.append("HeadYaw")
		mainState.name.append("HeadPitch")
		mainState.position.append(0.0)
		mainState.position.append(start)
		pub.publish(mainState)
		totalDistance = finish - start
		increment = totalDistance/splits
		time.sleep(.5)
		for i in range(splits):
			mainState.header.stamp = rospy.get_rostime()
			mainState.position[0] = 0
			mainState.position[1] = mainState.position[1] + increment
			pub.publish(mainState)
			time.sleep(.2)
		mainState.position[1]=start
		pub.publish(mainState)
		rate.sleep()	

	
	

if __name__ == '__main__':
	try:
		#Testing our function
		moveNao()
	except rospy.ROSInterruptException: passRAnklePitch