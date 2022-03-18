#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/UInt16.h>
#include <geometry_msgs/Twist.h>
#include <Wire.h>

#define BUTTON 8
#define LED 13

#define startbyte 0x0F
#define I2Caddress 0x07

int sv[6]={1500,1500,1500,1500,0,0};                 // servo positions: 0 = Not Used
int sd[6]={5,10,-5,-15,20,-20};                      // servo sweep speed/direction
int lmspeed,rmspeed;                                 // left and right motor speed from -255 to +255 (negative value = reverse)
int ldir=5;                                          // how much to change left  motor speed each loop (use for motor testing)
int rdir=5;                                          // how much to change right motor speed each loop (use for motor testing)
byte lmbrake,rmbrake;                                // left and right motor brake (non zero value = brake)
byte devibrate=50;                                   // time delay after impact to prevent false re-triggering due to chassis vibration
int sensitivity=50;                                  // threshold of acceleration / deceleration required to register as an impact
int lowbat=550;                                      // adjust to suit your battery: 550 = 5.50V
byte i2caddr=7;                                      // default I2C address of T'REX is 7. If this is changed, the T'REX will automatically store new address in EEPROM
byte i2cfreq=0;                                      // I2C clock frequency. Default is 0=100kHz. Set to 1 for 400kHz
String x;

ros::NodeHandle node_handle;

std_msgs::String button_msg;
geometry_msgs::Twist cmd_vel_msg

void subscriberCallback(const geometry_msgs::Twist& cmd_vel_msg) {
//  if (led_msg.data  == 1) {
//    digitalWrite(LED, HIGH); 
//  } else {
//    digitalWrite(LED, LOW);
//  }
//}

ros::Publisher button_publisher("button_press", &button_msg);
ros::Subscriber<std_msgs::UInt16> led_subscriber("cmd_vel", &subscriberCallback);


void setup()
{
  Serial.begin(9600);
  Wire.begin();                                      // no address - join the bus as master

  node_handle.initNode();
  node_handle.advertise(button_publisher);
  node_handle.subscribe(led_subscriber);
}


void loop()
{
  while(!Serial.available());
  // recieved data packet
  int rcvdData[17];
  // ready to flash the buffer
  bool flushBuff = false;
  // what index it is
  int index = 0;
  // character that marks the end of 
  char endmarker = '\n';
  // delimator
  char delim = ',';
  // string read from the end of , to the next ,
  String interimString;
  // recieved character
  char rc;
  // current integer
  int currentInt;
  while (Serial.available() > 0) {
    rc = Serial.read();
    
    if ((rc == delim || rc == endmarker) && flushBuff == false) {
      rcvdData[index] = interimString.toInt();
      interimString = "";
      index += 1;
      if (rc == endmarker) {
        flushBuff = true;
      }
    }
    else {
      interimString += rc;
    }
  }

//  for (int i = 0; i < 17; i++) {
//    Serial.println(rcvdData[i]);
//  }


  lmspeed = rcvdData[2];
//  Serial.println("Left motor speed");
//  Serial.println(lmspeed);
  lmbrake = rcvdData[3];
  rmspeed = rcvdData[4];
  rmbrake = rcvdData[5];
  sv[0] = rcvdData[6];
  sv[1] = rcvdData[7];
  sv[2] = rcvdData[8];
  sv[3] = rcvdData[9];
  sv[4] = rcvdData[10];
  sv[5] = rcvdData[11];
  devibrate = rcvdData[12];
  sensitivity = rcvdData[13];
  lowbat = rcvdData[14];
  i2caddr = rcvdData[15];
  i2cfreq = rcvdData[16];
  
       // send data packet to T'REX controller 
  MasterSend(startbyte,2,lmspeed,lmbrake,rmspeed,rmbrake,sv[0],sv[1],sv[2],sv[3],sv[4],sv[5],devibrate,sensitivity,lowbat,i2caddr,i2cfreq);
  delay(50);
  MasterReceive();                                   // receive data packet from T'REX controller
  delay(50);
  
  
  
//  //=================================================== Code to test motors and sweep servos =============================================  
//  lmspeed+=ldir;
//  if(lmspeed>240 or lmspeed<-240) ldir=-ldir;        // increase / decrease left motor speed and direction (negative values = reverse direction)
//  
//  rmspeed+=rdir;
//  if(rmspeed>240 or rmspeed<-240) rdir=-rdir;        // increase / decrease left motor speed and direction (negative values = reverse direction)
//  
//  lmbrake=(abs(lmspeed)>235);                        // test left  motor brake 
//  rmbrake=(abs(rmspeed)>235);                        // test right motor brake 
//  
//  for(byte i=0;i<6;i++)                              // sweep servos
//  {
//    if(sv[i]!=0)                                     // a value of 0 indicates no servo attached
//    {
//      sv[i]+=sd[i];                                  // update servo position to create sweeping motion
//      if(sv[i]>2000 || sv[i]<1000) sd[i]=-sd[i];     // reverse direction of servo if limit reached
//    }
//  }
}
