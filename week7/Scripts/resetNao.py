#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
jointPain = None

def reset():
	rospy.init_node('nao_movement', anonymous=True)
	pub = rospy.Publisher('joint_states', JointState, queue_size=10)
	rate = rospy.Rate(10)
	mainState = JointState()
	while not rospy.is_shutdown():
		mainState.header.stamp = rospy.get_rostime()
		mainState.header.frame_id = "TorsO"
		mainState.name.append("HeadYaw")
		mainState.name.append("HeadPitch")
		mainState.position.append(0)
		mainState.position.append(0)
		pub.publish(mainState)
		rate.sleep()


if __name__ == '__main__':
	try:
		#Testing our function
		reset()
	except rospy.ROSInterruptException: passRAnklePitch