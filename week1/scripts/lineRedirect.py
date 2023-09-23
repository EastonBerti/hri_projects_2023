#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
speed = 5
ASpeed = 1
PI = 3.1415926535897
angular_speed = ASpeed*45*PI/360
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
vel_msg = Twist()
stillFleeing = False    

def callback(data):
    rangerDan = data.ranges
    global speed
    global angular_speed
    global stillFleeing
    print(stillFleeing)
    for i in rangerDan:
        if not stillFleeing:
            if i < 0.85:
                speed = 0
                stillFleeing = True
                turnToward(rangerDan)
                speed = 1
                    
            else:
                randomElse = True

def turnToward(rangerDan):
    x = 0
    global speed
    global angular_speed
    global vel_msg
    global stillFleeing
    rightCount = 0
    leftCount = 0
    for i in rangerDan:
        if i > 8.0 and x < 541:
            rightCount = rightCount + 1
        elif i > 8.0:
            leftCount = leftCount + 1
        x = x+1
    if rightCount > leftCount:
        print("clockwise")
        vel_msg.angular.z = -abs(angular_speed)
    elif rightCount < leftCount:
        print("counterclockwise")
        vel_msg.angular.z =abs(angular_speed)
    print(rightCount)
    print(leftCount)
    for i in range(125000):
        pub.publish(vel_msg)
    vel_msg.angular.z = 0
    pub.publish(vel_msg)

    for k in range(20000):
        vel_msg.linear.x = 5
        pub.publish(vel_msg)
    vel_msg.linear.x = 0
    stillFleeing = False
    pub.publish(vel_msg)

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