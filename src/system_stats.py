#!/usr/bin/env python
import rospy
import rospkg
import numpy as np
import sys
from std_msgs.msg import String
import time
import ros_syslog.msg
import psutil
import subprocess

class ROS_System_Log:

   def __init__(self):
      
      self.num_cpus = psutil.cpu_count(logical=False)
      
      # ros publishers
      if self.num_cpus == 2:
         self.pub_syslog = rospy.Publisher('/SysLog', ros_syslog.msg.SystemStatsCPU2, queue_size=0)
    
      if self.num_cpus == 4:
         self.pub_syslog = rospy.Publisher('/SysLog', ros_syslog.msg.SystemStatsCPU4, queue_size=0)
    
      if self.num_cpus == 6:
         self.pub_syslog = rospy.Publisher('/SysLog', ros_syslog.msg.SystemStatsCPU6, queue_size=0)
    
      if self.num_cpus == 8:
         self.pub_syslog = rospy.Publisher('/SysLog', ros_syslog.msg.SystemStatsCPU8, queue_size=0)
    
      if self.num_cpus == 10:
         self.pub_syslog = rospy.Publisher('/SysLog', ros_syslog.msg.SystemStatsCPU10, queue_size=0)
   

      # callback on timer
      self.data_collect_hz = float(rospy.get_param("~collect_hz", 10.0))
      
      rospy.Timer(rospy.Duration((1.0/self.data_collect_hz)), self.log_system)

   def log_system(self, event):
      cpu_percentages = psutil.cpu_percent(percpu=True)
      cpu_temperature = psutil.sensors_temperatures()["coretemp"]
      net = subprocess.Popen(["cat", "/proc/net/wireless"], stdout=subprocess.PIPE).communicate()[0].split('\n')[2].split()[3]

      if self.num_cpus == 2:
         RSL_msg = ros_syslog.msg.SystemStatsCPU2()
    
      if self.num_cpus == 4:
         RSL_msg = ros_syslog.msg.SystemStatsCPU4()
    
      if self.num_cpus == 6:
         RSL_msg = ros_syslog.msg.SystemStatsCPU6()
    
      if self.num_cpus == 8:
         RSL_msg = ros_syslog.msg.SystemStatsCPU8()
    
      if self.num_cpus == 10:
         RSL_msg = ros_syslog.msg.SystemStatsCPU10()
   
      
      RSL_msg.header.stamp = rospy.get_rostime()
      RSL_msg.net_percent = np.int8(np.round(((float(net)+110)*10.0)/7.0))
      RSL_msg.net_RSSI_dBm = np.int8(np.round(float(net)))
      RSL_msg.temp_package = np.int8(np.round(cpu_temperature[0].current))
      RSL_msg.temp_core_0 = np.int8(np.round(cpu_temperature[1].current))
      RSL_msg.temp_core_1 = np.int8(np.round(cpu_temperature[2].current))
      RSL_msg.cpu_percent = np.int8(np.round(np.average(cpu_percentages)))
      RSL_msg.percent_0 = np.int8(np.round(cpu_percentages[0]))
      RSL_msg.percent_1 = np.int8(np.round(cpu_percentages[1]))

      if self.num_cpus > 2:
         RSL_msg.temp_core_2 = np.int8(np.round(cpu_temperature[3].current))
         RSL_msg.temp_core_3 = np.int8(np.round(cpu_temperature[4].current))
         RSL_msg.percent_2 = np.int8(np.round(cpu_percentages[2]))
         RSL_msg.percent_3 = np.int8(np.round(cpu_percentages[3]))
         
         if self.num_cpus > 4:
            RSL_msg.temp_core_4 = np.int8(np.round(cpu_temperature[5].current))
            RSL_msg.temp_core_5 = np.int8(np.round(cpu_temperature[6].current))
            RSL_msg.percent_4 = np.int8(np.round(cpu_percentages[4]))
            RSL_msg.percent_5 = np.int8(np.round(cpu_percentages[5]))
            
            if self.num_cpus > 6:
               RSL_msg.temp_core_6 = np.int8(np.round(cpu_temperature[7].current))
               RSL_msg.temp_core_7 = np.int8(np.round(cpu_temperature[8].current))
               RSL_msg.percent_6 = np.int8(np.round(cpu_percentages[6]))
               RSL_msg.percent_7 = np.int8(np.round(cpu_percentages[7]))
               
               if self.num_cpus > 8:
                  RSL_msg.temp_core_8 = np.int8(np.round(cpu_temperature[9].current))
                  RSL_msg.temp_core_9 = np.int8(np.round(cpu_temperature[10].current))
                  RSL_msg.percent_8 = np.int8(np.round(cpu_percentages[8]))
                  RSL_msg.percent_9 = np.int8(np.round(cpu_percentages[9]))
      
      self.pub_syslog.publish(RSL_msg)
      return


def main(args):
    "main function"
    rospy.init_node('ros_syslog_node')
    rospy.loginfo("RSL: Starting up")
    ld = ROS_System_Log()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("RSL: Shutting down")


if __name__ == '__main__':
    main(sys.argv)
