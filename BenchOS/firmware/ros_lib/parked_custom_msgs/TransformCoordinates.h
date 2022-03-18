#ifndef _ROS_SERVICE_TransformCoordinates_h
#define _ROS_SERVICE_TransformCoordinates_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "parked_custom_msgs/Point.h"

namespace parked_custom_msgs
{

static const char TRANSFORMCOORDINATES[] = "parked_custom_msgs/TransformCoordinates";

  class TransformCoordinatesRequest : public ros::Msg
  {
    public:
      uint8_t inputPositions_length;
      parked_custom_msgs::Point st_inputPositions;
      parked_custom_msgs::Point * inputPositions;
      uint32_t flag;
      enum { LONG_MIN =  0.0 };
      enum { LONG_MAX =  1.2631578947 };
      enum { LAT_MIN =  0.0 };
      enum { LAT_MAX =  1.0 };
      enum { IMAGE_X =  1200 };
      enum { IMAGE_Y =  950 };

    TransformCoordinatesRequest():
      inputPositions_length(0), inputPositions(NULL),
      flag(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset++) = inputPositions_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( uint8_t i = 0; i < inputPositions_length; i++){
      offset += this->inputPositions[i].serialize(outbuffer + offset);
      }
      *(outbuffer + offset + 0) = (this->flag >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->flag >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->flag >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->flag >> (8 * 3)) & 0xFF;
      offset += sizeof(this->flag);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint8_t inputPositions_lengthT = *(inbuffer + offset++);
      if(inputPositions_lengthT > inputPositions_length)
        this->inputPositions = (parked_custom_msgs::Point*)realloc(this->inputPositions, inputPositions_lengthT * sizeof(parked_custom_msgs::Point));
      offset += 3;
      inputPositions_length = inputPositions_lengthT;
      for( uint8_t i = 0; i < inputPositions_length; i++){
      offset += this->st_inputPositions.deserialize(inbuffer + offset);
        memcpy( &(this->inputPositions[i]), &(this->st_inputPositions), sizeof(parked_custom_msgs::Point));
      }
      this->flag =  ((uint32_t) (*(inbuffer + offset)));
      this->flag |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->flag |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->flag |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->flag);
     return offset;
    }

    const char * getType(){ return TRANSFORMCOORDINATES; };
    const char * getMD5(){ return "17d0f45dd1be1f005c3d0c8a3532b544"; };

  };

  class TransformCoordinatesResponse : public ros::Msg
  {
    public:
      uint8_t processedPositions_length;
      parked_custom_msgs::Point st_processedPositions;
      parked_custom_msgs::Point * processedPositions;

    TransformCoordinatesResponse():
      processedPositions_length(0), processedPositions(NULL)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset++) = processedPositions_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( uint8_t i = 0; i < processedPositions_length; i++){
      offset += this->processedPositions[i].serialize(outbuffer + offset);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint8_t processedPositions_lengthT = *(inbuffer + offset++);
      if(processedPositions_lengthT > processedPositions_length)
        this->processedPositions = (parked_custom_msgs::Point*)realloc(this->processedPositions, processedPositions_lengthT * sizeof(parked_custom_msgs::Point));
      offset += 3;
      processedPositions_length = processedPositions_lengthT;
      for( uint8_t i = 0; i < processedPositions_length; i++){
      offset += this->st_processedPositions.deserialize(inbuffer + offset);
        memcpy( &(this->processedPositions[i]), &(this->st_processedPositions), sizeof(parked_custom_msgs::Point));
      }
     return offset;
    }

    const char * getType(){ return TRANSFORMCOORDINATES; };
    const char * getMD5(){ return "3cfdd1b08ba5cf8b4e3ab160323f98b4"; };

  };

  class TransformCoordinates {
    public:
    typedef TransformCoordinatesRequest Request;
    typedef TransformCoordinatesResponse Response;
  };

}
#endif
