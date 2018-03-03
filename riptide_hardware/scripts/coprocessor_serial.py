#!/usr/bin/env python

import serial
import rospy
from std_msgs.msg import String
from riptide_msgs.msg import Depth
from riptide_msgs.msg import PwmStamped
from riptide_msgs.msg import SwitchState

COM_PORT = '/dev/ttyACM0'
ser = serial.Serial(COM_PORT, baudrate=9600, timeout=None)

def pwm_callback(pwm_message):
    #The Start and End bytes for a PWM Message
    pwmStart = "####"
    pwmEnd = "@@@@"

    #Each thruster's pwm value is stored
    ssh = str(pwm_message.pwm.surge_stbd_hi)
    sph = str(pwm_message.pwm.surge_port_hi)
    spl = str(pwm_message.pwm.surge_port_lo)
    ssl = str(pwm_message.pwm.surge_stbd_lo)
    swf = str(pwm_message.pwm.sway_fwd)
    swa = str(pwm_message.pwm.sway_aft)
    hpa = str(pwm_message.pwm.heave_port_aft)
    hsa = str(pwm_message.pwm.heave_stbd_aft)
    hsf = str(pwm_message.pwm.heave_stbd_fwd)
    hpf = str(pwm_message.pwm.heave_port_fwd)

    #The pwm values and start and end bytes are added to a String and written
    final_pwm = pwmStart + ssh + sph + spl + ssl + swf + swa + hpa + hsa + hsf + hpf + pwmEnd
    final_pwm = bytes(final_pwm)
    ser.write(final_pwm)

def main():
    rospy.init_node('coprocessor_serial')
    dataRead = True;

    #Subscribe to Thruster PWMs
    rospy.Subscriber("/command/pwm", PwmStamped, pwm_callback)
    rospy.spin()

    while not rospy.is_shutdown():

        switchData = []
        depthData =""
        if ser is not None:
            dataRead = True
            depthRead = False
            swRead = False

            while dataRead:
                data = ser.read();
                if data is not "":

                    #First two conditions check for start bytes
                    if (data == "%"):
                        depthRead = True
                    elif(data == "$"):
                        swRead = True
                    else:
                        if(depthRead):
                            if(data == "@"):
                                #End byte recieved
                                depthRead = False
                                dataRead = False
                            else:
                                depthData = depthData + data

                        if(swRead):
                            if(data == "@"):
                                #End byte recieved
                                swRead = False
                                dataRead = False
                            else:
                                try:
                                    switchData.append(data)
                                except "n":
                                    print "Error - switch not detected"
                                    sys.exit()


        depthList = depthData.split("!")
        msg.pressure = depthList[0]
        msg.temp = depthList[1]
        msg.depth = depthList[2]
        
        depthPub = rospy.Publisher('/state/depth', std_msgs.msg.String, queue_size=10)
        depthPub.publish(msg);

        msg.kill = switchData[0]
        msg.sw1 = switchData[1]
        msg.sw2 = switchData[2]
        msg.sw3 = switchData[3]
        msg.sw4 = switchData[4]
        msg.sw5 = switchData[5]
        swPub = rospy.Publisher('/state/switches', std_msgs.msg.String, queue_size=10)
        swPub.publish(msg);

if __name__ == "__main__": main()
