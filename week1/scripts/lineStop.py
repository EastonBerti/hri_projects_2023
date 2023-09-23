#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
speed = 1

def callback(data):
    rangerDan = data.ranges
    x = 0
    global speed
    for i in rangerDan:
        x = x + 1
        if i < 0.85:
            print("Stop! Collision range at " + str(x))
            speed = 0
            rospy.signal_shutdown("Collision Imminent")
            return 0
        else:
            randomElse = True
    
def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    rospy.Subscriber("/base_scan", LaserScan, callback)
    
    
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0    
    
    while not rospy.is_shutdown():
        vel_msg.linear.x = abs(speed)
        for i in range(75000):
            vel_msg.linear.x = abs(speed)
            pub.publish(vel_msg)
        vel_msg.linear.x = 0
        pub.publish(vel_msg)
    rospy.spin()
if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass