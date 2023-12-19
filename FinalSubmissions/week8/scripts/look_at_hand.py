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
    start0 = -1.0
    finish0 = .17
    start1 = 0.5
    finish1 = -0.39
    splits = 20
    while not rospy.is_shutdown():
        mainState.header.stamp = rospy.get_rostime()
        mainState.header.frame_id = "Torso"
        mainState.name.append("HeadYaw")
        mainState.name.append("HeadPitch")
        mainState.position.append(start0)
        mainState.position.append(start1)
        pub.publish(mainState)
        totalDistance0 = finish0 - start0
        totalDistance1 = finish1 - start1
        increment0 = totalDistance0/splits
        increment1 = totalDistance1/splits
        time.sleep(.5)
        for i in range(splits):
            mainState.header.stamp = rospy.get_rostime()
            mainState.position[0] = mainState.position[1] + increment0
            mainState.position[1] = mainState.position[1] + increment1
            pub.publish(mainState)
            time.sleep(.2)
        mainState.position[0]=-start0
        mainState.position[1]=start1
        pub.publish(mainState)
        rate.sleep()    

    
    

if __name__ == '__main__':
    try:
        #Testing our function
        moveNao()
    except rospy.ROSInterruptException: passRAnklePitch