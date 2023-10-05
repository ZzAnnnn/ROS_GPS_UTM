#!/usr/bin/env python3
import rospy
import serial
import utm
import sys
from lab1_gps.msg import multi_msg

def gps_data_pub():
    gps_pub = rospy.Publisher('gps_out', multi_msg, queue_size=10)

    rospy.init_node('gps_data_publisher', anonymous=True)

    msg = multi_msg()

    args = rospy.myargv(argv =sys.argv)
    port = rospy.get_param('~port',args[1])

    serial_port = serial.Serial(port, baudrate=4800)

    while not rospy.is_shutdown():

        gps_data = str(serial_port.readline())

        if "$GPGGA" in str(gps_data):
          data = str(gps_data).split(",")
          print(data)

          timestamp = float(data[1])

          lat_raw = float(data[2])
          lat_int = int(lat_raw/100)
          lat_decimal = float(lat_raw) - (lat_int*100)
          lat = float(lat_int+lat_decimal/60)
          if data[3] == 'S':
            lat = lat*(-1)
          
          long_raw = float(data[4])
          long_int = int(long_raw/100)
          long_decimal = float(long_raw) - (long_int*100)
          long = float(long_int+long_decimal/60)
          if data[5] =='W':
            long = long*(-1)

          utm_coords = utm.from_latlon(lat,long)
          
          msg.header.stamp.secs = int(timestamp)
          msg.header.frame_id = 'GPS1_Frame'
          msg.latitude = lat
          msg.longtitude = long
          msg.altitude = float(data[9])
          msg.utm_easting = utm_coords[0]
          msg.utm_northing = utm_coords[1]
          msg.zone = utm_coords[2]
          msg.letter = utm_coords[3]

          gps_pub.publish(msg)

if __name__ =='__main__':
    try:
      gps_data_pub()
    except rospy.ROSInterruptException:
        pass
