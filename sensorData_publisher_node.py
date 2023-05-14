#!/usr/bin/env python

import json
import requests 
import rospy
from std_msgs.msg import String

# This will get sensor data from the arduino webserver and will convert each sensor's
# range data into a type that can be published to a ROS topic called talker. 
def sensor_publisher():

    pub = rospy.Publisher('talker', String, queue_size=10)
    rospy.init_node('publisher_node', anonymous = True)
    rate = rospy.Rate(1)
    rospy.loginfo("Publisher node started and will publish sensor data")

    while not rospy.is_shutdown():
        url = 'http://192.168.1.5'
        r = requests.get(url, stream = True)  

        data = json.loads(r.text)

        # typecasting individual data points into a string
        dataSensorOne = str(data["sensor1"])
        dataSensorTwo = str(data["sensor2"])

        # Publish: typecasted sensor data for sensor one and then two
        pub.publish("1: " + dataSensorOne + " || " + "2: " + dataSensorTwo)
        rate.sleep()

        # Other ways that the data could be published
            # typecast the entire python dict (which we got through json.loads) to a str
            #   pub.publish(str(data))
            # publish each previously typecasted sensor data seperately
            #   pub.publish("1: " + dataSensorOne)
            #   pub.publish("2: " + dataSensorTwo)


if __name__ == '__main__':
    try:
        sensor_publisher()
    except rospy.ROSInterruptException:
        pass
