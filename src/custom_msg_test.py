import rospy
from shakebot_motion.msg import calib_msg


if __name__ == '__main__':

    rospy.init_node('calib_msg_test', anonymous=True)
    pub = rospy.Publisher('calib_msg', calib_msg, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = calib_msg()
        msg.left_ls = 1
        msg.right_ls = 1
        msg.bed_length = 0.5

        pub.publish(msg)