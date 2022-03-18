#ifndef _ROS_parked_custom_msgs_Robot_Sensor_State_h
#define _ROS_parked_custom_msgs_Robot_Sensor_State_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "parked_custom_msgs/Compass.h"
#include "parked_custom_msgs/Ultrasonic_Sensor.h"

namespace parked_custom_msgs
{

  class Robot_Sensor_State : public ros::Msg
  {
    public:
      parked_custom_msgs::Compass Compass;
      parked_custom_msgs::Ultrasonic_Sensor UltrasonicFLeft;
      parked_custom_msgs::Ultrasonic_Sensor UltrasonicFRight;
      parked_custom_msgs::Ultrasonic_Sensor UltrasonicBack;

    Robot_Sensor_State():
      Compass(),
      UltrasonicFLeft(),
      UltrasonicFRight(),
      UltrasonicBack()
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->Compass.serialize(outbuffer + offset);
      offset += this->UltrasonicFLeft.serialize(outbuffer + offset);
      offset += this->UltrasonicFRight.serialize(outbuffer + offset);
      offset += this->UltrasonicBack.serialize(outbuffer + offset);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->Compass.deserialize(inbuffer + offset);
      offset += this->UltrasonicFLeft.deserialize(inbuffer + offset);
      offset += this->UltrasonicFRight.deserialize(inbuffer + offset);
      offset += this->UltrasonicBack.deserialize(inbuffer + offset);
     return offset;
    }

    const char * getType(){ return "parked_custom_msgs/Robot_Sensor_State"; };
    const char * getMD5(){ return "8c525d82fcbf3cea463facd47176a440"; };

  };

}
#endif