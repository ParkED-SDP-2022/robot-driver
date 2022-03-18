#ifndef _ROS_parked_custom_msgs_Point_h
#define _ROS_parked_custom_msgs_Point_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace parked_custom_msgs
{

  class Point : public ros::Msg
  {
    public:
      float long;
      float lat;
      float angle;

    Point():
      long(0),
      lat(0),
      angle(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += serializeAvrFloat64(outbuffer + offset, this->long);
      offset += serializeAvrFloat64(outbuffer + offset, this->lat);
      offset += serializeAvrFloat64(outbuffer + offset, this->angle);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += deserializeAvrFloat64(inbuffer + offset, &(this->long));
      offset += deserializeAvrFloat64(inbuffer + offset, &(this->lat));
      offset += deserializeAvrFloat64(inbuffer + offset, &(this->angle));
     return offset;
    }

    const char * getType(){ return "parked_custom_msgs/Point"; };
    const char * getMD5(){ return "8dfb3d924804e67d0d12ca47a9ea9644"; };

  };

}
#endif