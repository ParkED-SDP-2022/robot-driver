
void MasterReceive()
{//================================================================= Error Checking ==========================================================
  byte d;
  int i=0;
  Wire.requestFrom(I2Caddress,24);                                // request 24 bytes from device 007
  
  while(Wire.available()<24)                                      // wait for entire data packet to be received
  {
    if(i==0) Serial.print("Waiting for slave to send data.");     // Only print message once (i==0)
    if(i>0) Serial.print(".");                                    // print a dot for every loop where buffer<24 bytes
    i++;                                                          // increment i so that message only prints once.
    if(i>79)
    {
      Serial.println("");
      i=1;
    }
  }
  d=Wire.read();                                                  // read start byte from buffer
  if(d!=startbyte)                                                // if start byte not equal to 0x0F                                                    
  {
    Serial.print(d,DEC);
    while(Wire.available()>0)                                     // empty buffer of bad data
    {
      d=Wire.read();
    }
    Serial.println("  Wrong Start Byte");                         // error message
    return;                                                       // quit
  }
  
  //================================================================ Read Data ==============================================================
  int data[12];
  data[0] = 15;
  
//  Serial.print("Slave Error Message:");                           // slave error report
//  Serial.println(Wire.read(),DEC);
  int x = Wire.read();
  data[1] = x;
  
  i=Wire.read()*256+Wire.read();                                  // T'REX battery voltage
  data[2] = i;
//  Serial.print("Battery Voltage:\t");
//  Serial.print(int(i/10));Serial.println(".");                      
//  Serial.print(i-(int(i/10)*10));Serial.println("V");
  
  i=Wire.read()*256+Wire.read();
  data[3] = i;
//  Serial.print("Left  Motor Current:\t");
//  Serial.print(i);Serial.println("mA");                           // T'REX left  motor current in mA
  
  i=Wire.read()*256+Wire.read();
  data[4] = i;
//  Serial.print("Left  Motor Encoder:\t");
//  Serial.println(i);                                              // T'REX left  motor encoder count
  
  i=Wire.read()*256+Wire.read();
//  Serial.print("Right Motor Current:\t");
//  Serial.print(i);Serial.println("mA");                           // T'REX right motor current in mA
  
  i=Wire.read()*256+Wire.read();
  data[5] = i;
//  Serial.print("Right Motor Encoder:\t");
//  Serial.println(i);                                              // T'REX right motor encoder count
  
  i=Wire.read()*256+Wire.read();
  data[6] = i;
//  Serial.print("X-axis:\t\t");
//  Serial.println(i);                                              // T'REX X-axis
  
  i=Wire.read()*256+Wire.read();
  data[7] = i;
//  Serial.print("Y-axis:\t\t");
//  Serial.println(i);                                              // T'REX Y-axis
  
  i=Wire.read()*256+Wire.read();
  data[8] = i;
//  Serial.print("Z-axis:\t\t");
//  Serial.println(i);                                              // T'REX Z-axis
  
  i=Wire.read()*256+Wire.read();
  data[9] = i;
//  Serial.print("X-delta:\t\t");
//  Serial.println(i);                                              // T'REX X-delta
  
  i=Wire.read()*256+Wire.read();
  data[10] = i;
//  Serial.print("Y-delta:\t\t");
//  Serial.println(i);                                              // T'REX Y-delta
  
  i=Wire.read()*256+Wire.read();
  data[11] = i;
//  Serial.print("Z-delta:\t\t");
//  Serial.println(i);                                              // T'REX Z-delta
//  Serial.print("\r\n\n\n");

//  Serial.println("packet started");

  for(int i=0; i<sizeof(data) / sizeof(data[0]); i++)
   {
      Serial.print(data[i]);
      if (i != sizeof(data)) {
        Serial.print(",");
      }
      
      
   }
   Serial.println("\n");
//   Serial.println("Packet finished");
  
}
  
  
  
  
  
  
  
