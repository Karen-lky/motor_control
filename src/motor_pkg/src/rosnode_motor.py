#!/usr/bin/env python
import rospy
from simple_pid import PID
from std_msgs.msg import Int64
from std_msgs.msg import Float64
from std_msgs.msg import Int16

#predefined some parameter based on assumption
PWM_Output = 0
PPR = 41
gearRatio = 60
encoderTicks = 0
started_encoderTicks = False
started_targetPosition = False
TargetPosition_angle = 0.0
current_angle = 0

#publish the targetposition in angle and also the motorpwm 
pub = rospy.Publisher('/motorPwm',Int16,queue_size=100)
pub1 = rospy.Publisher('/TargetPosition',Int16,queue_size=100)

#define the function for callback for subscipting the topics for /encoderTicks & /received_targetPosition
def sub_encoderTicks():
    rospy.init_node('node_controlMotor', anonymous=True)
    rospy.Subscriber('encoderTicks',Int64,callback_encoder)
    rospy.Subscriber('received_targetPosition',Float64,callback_target)
    timer = rospy.Timer(rospy.Duration(0.01),timer_callback)
    rospy.spin()
    timer.shutdown()

def callback_encoder(data):
    global started_encoderTicks,encoderTicks
    print("EncoderValue Received",encoderTicks)
    encoderTicks = data.data
    #if (not started_encoderTicks):
    #    started_encoderTicks = True

def callback_target(data):
    global started_targetPosition,TargetPosition_angle
    TargetPosition_angle = data.data
    #if (not started_targetPosition):
    #    TargetPosition_angle = True

#define the callback function to calculate the PID output to update the topics 
#and feed to microcontroller via motorpwm.
def timer_callback(event):
    global started_encoderTicks,started_targetPosition,pub,encoderTicks,PWM_Output,TargetPosition_angle,current_angle #,current_wheel_distance
    
    #condition when info targetPosition and EncoderTicks received and do the following
    #However, due to missing constant feedback on /EncoderTicks, it does not work in this way.
    #if(started_targetPosition):
    #    if (started_encoderTicks):

    previous_angle=current_angle
    pid = PID(0.022,0.01,2,setpoint=TargetPosition_angle)
    pid.output_limits = (-255, 255)
    pid.sample_time = 0.001
    PWM_Output = pid(previous_angle)

    if( 0 < PWM_Output <= 13):
        PWM_Output = PWM_Output + 11.5
    elif (-13 <= PWM_Output < 0):
        PWM_Output = PWM_Output - 11.5
    
    current_angle = encoderTicks/24
    
    pub.publish(PWM_Output)
    
    print("Publishing PWM Values",PWM_Output)
    print("Current angle",current_angle)
    print("Desired Position",TargetPosition_angle)
    print("==================================================")

    #reduce the display data
    rate = rospy.Rate(0.5)
    rate.sleep()


if __name__ == '__main__':
    #activate to check program started
    print("Running")
    #start the function to pub and sub the topics
    sub_encoderTicks()




