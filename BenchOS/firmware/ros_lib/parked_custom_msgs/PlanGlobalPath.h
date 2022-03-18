#ifndef _ROS_SERVICE_PlanGlobalPath_h
#define _ROS_SERVICE_PlanGlobalPath_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "parked_custom_msgs/Point.h"

namespace parked_custom_msgs
{

static const char PLANGLOBALPATH[] = "parked_custom_msgs/PlanGlobalPath";

  class PlanGlobalPathRequest : public ros::Msg
  {
    public:
      parked_custom_msgs::Point current_position;
      parked_custom_msgs::Point destination;
      uint8_t constraints_length;
      parked_custom_msgs::Point st_constraints;
      parked_custom_msgs::Point * constraints;

    PlanGlobalPathRequest():
      current_position(),
      destination(),
      constraints_length(0), constraints(NULL)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->current_position.serialize(outbuffer + offset);
      offset += this->destination.serialize(outbuffer + offset);
      *(outbuffer + offset++) = constraints_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( uint8_t i = 0; i < constraints_length; i++){
      offset += this->constraints[i].serialize(outbuffer + offset);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->current_position.deserialize(inbuffer + offset);
      offset += this->destination.deserialize(inbuffer + offset);
      uint8_t constraints_lengthT = *(inbuffer + offset++);
      if(constraints_lengthT > constraints_length)
        this->constraints = (parked_custom_msgs::Point*)realloc(this->constraints, constraints_lengthT * sizeof(parked_custom_msgs::Point));
      offset += 3;
      constraints_length = constraints_lengthT;
      for( uint8_t i = 0; i < constraints_length; i++){
      offset += this->st_constraints.deserialize(inbuffer + offset);
        memcpy( &(this->constraints[i]), &(this->st_constraints), sizeof(parked_custom_msgs::Point));
      }
     return offset;
    }

    const char * getType(){ return PLANGLOBALPATH; };
    const char * getMD5(){ return "8bae0594a47ca11bfaaf5407027bab58"; };

  };

  class PlanGlobalPathResponse : public ros::Msg
  {
    public:
      uint8_t path_length;
      parked_custom_msgs::Point st_path;
      parked_custom_msgs::Point * path;

    PlanGlobalPathResponse():
      path_length(0), path(NULL)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset++) = path_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( uint8_t i = 0; i < path_length; i++){
      offset += this->path[i].serialize(outbuffer + offset);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint8_t path_lengthT = *(inbuffer + offset++);
      if(path_lengthT > path_length)
        this->path = (parked_custom_msgs::Point*)realloc(this->path, path_lengthT * sizeof(parked_custom_msgs::Point));
      offset += 3;
      path_length = path_lengthT;
      for( uint8_t i = 0; i < path_length; i++){
      offset += this->st_path.deserialize(inbuffer + offset);
        memcpy( &(this->path[i]), &(this->st_path), sizeof(parked_custom_msgs::Point));
      }
     return offset;
    }

    const char * getType(){ return PLANGLOBALPATH; };
    const char * getMD5(){ return "236c17deca12468ed68daa7e4fd3e493"; };

  };

  class PlanGlobalPath {
    public:
    typedef PlanGlobalPathRequest Request;
    typedef PlanGlobalPathResponse Response;
  };

}
#endif
