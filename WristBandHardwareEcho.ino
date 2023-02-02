//This is the hardware program from Samuel Gandy in Group 7
//for unit ENG500 Group Project


#include <ESP8266WiFi.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LIS3DH.h>
#include <SPI.h>
#include <Wire.h>
#include <SoftwareSerial.h> //softwareSerial allows for the functions to read the rx and tx
#include <Adafruit_GPS.h> //added the GPS libaray

//setup of functions

//GPS declare
void configAcc();
void configHeart();
void configGPS();
int readAcc();
int readHeart();
int readGPS(String GPSresult, int ESPlatitude, char HemisphereLat, int ESPlongitude, char HemisphereLon);

//Declare Accelometer variables below

#define LIS3DH_CLK 13 
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10

// software SPI
//Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS, LIS3DH_MOSI, LIS3DH_MISO, LIS3DH_CLK);
// hardware SPI
//Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS);
// I2C
Adafruit_LIS3DH lis = Adafruit_LIS3DH(); //set the lis variable to the adadfruit-LIS3DH function that reads the bits and turns them into digital values

//Declare HeartBeat varibales below

int AnalogValue = 0; //Declare analogValue
int AnalogPin = A0; //set the Heart beat sensor value

int count = 1; //set the count variable that counts the loops of the heart beat
int HeartTotal; //heart totel varaible set
int avgHeart = 0; //avage heart beat varaible declared
int Maxium = 0; //variable to equal the varaible
int compHeart = 0; //the variable all tyhe maxiums together equals
int MaxiumCount = 0; //max count is the maxium of loop
int learntavg = 0; //learnt average is the value of all averages of 100
int upperThreshold = 100; //threshold value equals 100
int midThreshold = 50; //midThreshold is equal 50
char episode = 'G'; //episode value is equal to char G at the start
String user = "User"; //user equals user
String Name = "Samuel"; //Name equals Samuel

//Declare GPS variables below

SoftwareSerial mySerial(14,12); //creating a serial port on pins 13 and 12 (Other ESP 14 and 12)
Adafruit_GPS GPS(&mySerial); //creating variable for GPS object and the & symbal is for the address

String NMEA1; //Variable for first NMEA sentance
String NMEA2; //Variable for second NMEA sentance
char c; //read charctures for the GPS

String GPSresult = ""; //SG


//dweet Protocol Variables
const char* ssid     = "iPhone";  //the name of network iPhone
const char* password = "1cwj0rv7zh4tk"; // Network password 

const char* host = "www.dweet.io"; //name of the server in this case dweet
const char* thing  = "group"; //The indvual key that the dweet gets sent to on the network allows for multiple dweets to be sent to different serves on the network

const char* AccXthing = "AccX"; //name before the value in dweet for X, Y and Z
const char* AccYthing = "AccY";
const char* AccZthing = "AccZ";

const char* GPSthing =  "GPS"; //name before value in GPS in dweet

const char* Heartthing = "Heartrate"; //the name before heart beat in string in dweet
 

void setup() {
  Serial.begin(9600); //set the bund rate to 9600 setting the commucations to computer to 9600 bytes a second
  Serial.println("System working"); //print system working on the monitor

  configTransmit(); //call setup for transmitter function

  configAcc(); //call setup the acceleromete function

  pinMode(AnalogPin, INPUT); //set the heart beat pin as an input
  
  configGPS(); //call function to call GPS

}

void loop() {
  Serial.println("Start of loop"); //start the loop

  readAcc(); //call function to read Acc
  readHeart(); //call function to read heart beat sensor
  readGPS(); //read the GPS

  Serial.print("connecting to "); //show connecting to on console
  Serial.println(host); //print the network name
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client; //[4]set the webclient up 
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  } //[4] ends here
  
  //Put GPS in to one String SG
  //There is a rounding error here i need to fix
  GPSresult += GPS.latitude,4; //add the number as a string
  GPSresult += GPS.lat; //add the char for the hemisphere
  GPSresult += ","; //add commer to break up the two values
  GPSresult += GPS.longitude,4; //add the number as the string
  GPSresult += GPS.lon; //add the char for the hemisphere

  Serial.print("Final GPS = "); Serial.println(GPSresult); //print final GPS values
  
  //Collecting all values and putting them into one dweet SG

  String URL = "/dweet/for/"; //[4] 
  URL += thing; //[4]
  URL += "?"; //[4]
  URL += user; //add user to string
  URL += "="; //add equals for dweet URL format
  URL += Name; //add name variable as string to the end of current URL
  URL += "&"; //add & to the string to space varaibles
  URL += AccXthing; //add X axis sensor name to string
  URL += "="; //add equals for dweet URL format
  URL += lis.x; //add X axis variable as string to the end of current URL
  URL += "&"; //add & to the string to space sensors and values in dweet
  URL += AccYthing; //add Y axis sensor name to string
  URL += "="; //add equals for dweet URL format
  URL += lis.y; //add Y axis variable as string to the end of current URL
  URL += "&"; //add & to the string to space sensors and values in dweet
  URL += AccZthing; //add Z axis sensor name to string
  URL += "="; //add equals for dweet URL format
  URL += lis.z; //add Y axis variable as string to the end of current URL
  URL += "&"; //add & to the string to space sensors and values in dweet
  URL += GPSthing; //add GPS name to string
  URL += "="; //add equals for dweet URL format
  URL += GPSresult; //add GPS result to the dweet string
  URL += "&"; //This will be included when heart beat is added
  URL += Heartthing; //Add sensor name for Heart beat to the dweet
  URL += "=";//add equals for dweet URL format
  URL += episode;//add episode value to the end of the URL
//[4]
  Serial.print("Requesting URL: ");
  Serial.println(URL);
  
  // This will send the request to the server
  client.print(String("GET ") + URL + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
  int timeout = millis() + 5000;
  while (client.available() == 0) {
    if (timeout - millis() < 0) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }
  
  // Read all the lines of the reply from server and print them to Serial
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("closing connection");
  //[4] ends here
  GPSresult = ""; //reset the string
}


void configTransmit(){ 
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  //[4]
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  //[4] ends here
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void configAcc(){
  //[3]
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("LIS3DH test!");
  
  if (lis.begin(0x18)) {   // change this to 0x19 for alternative i2c address
    Serial.println("LIS3DH found!");
  
  lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!
  
  Serial.print("Range = "); Serial.print(2 << lis.getRange());  
  Serial.println("G");
  //[3]
  }
}

int readAcc(){
  lis.read();      // get X Y and Z data at once
  // Then print out the raw data
  Serial.print("X:  "); Serial.print(lis.x);  //print the X is then a lis.X which is the function above reading the X of the Accelerometer registers 
  Serial.print("  \tY:  "); Serial.print(lis.y);  //print the Y is then a lis.X which is the function above reading the Y of the Accelerometer registers 
  Serial.print("  \tZ:  "); Serial.print(lis.z);  //print the Z is then a lis.X which is the function above reading the Z of the Accelerometer registers 
  Serial.println(" "); //set new line
  delay(200); //delay to allow to read values and print
  return lis.x,lis.y,lis.z; //return the values to the main loop
}

int readHeart(){
  while (count < 100){
    AnalogValue = analogRead(AnalogPin); //read the analog signal
    HeartTotal += AnalogValue; //add to the total for this set
    if(HeartTotal < 0){ //if the total is below 0 (when system is not on wrist)
      HeartTotal = 0; //set it to 0
    } 
    avgHeart = HeartTotal/(count); //Work out the mean
    Serial.print(count); Serial.print(" Heart Total = "); Serial.print(HeartTotal); Serial.print(" || "); Serial.print("Avg = "); Serial.println(avgHeart); //print Average

    count++; //add one to count
    delay(25); //lower the value the better becuase the hearts cycle is about 1 a second
  }
  Maxium = avgHeart; //stores the maxium
  count = 1; //set count back to 1 for new set
  HeartTotal = 0; //Heart Total is reset
  MaxiumCount++; //Maxium count plus one to look at new sets
  compHeart += Maxium; //plus the maxium to the compare heart value
  learntavg = compHeart/MaxiumCount; //learnt average equals the
  if(avgHeart > (learntavg + midThreshold) && avgHeart < (learntavg + upperThreshold)){ //if the avgHeart is way above the normal and below meltdown
    Serial.println("There could be an episode"); //print there is an episode
    episode = 'M';
  }
  if(avgHeart > (learntavg + upperThreshold)){ //if the avgHeart is way above the normal
    Serial.println("There is an Epsoide"); //print there is an episode
    episode = 'R'; //set char to R for episode
  }
  if(avgHeart < (learntavg + midThreshold)){
    Serial.println("All good");
    episode = 'G'; //set char to G for the student is all ok
 }
    
  Serial.print("Episode Value = "); Serial.println(episode);
  return episode;
}

//[1]
void configGPS(){
  GPS.begin(9600); //turn on GPS at 9600 bits by second
  //Need to clean the signal from teh antana to the GPS
  GPS.sendCommand("PGCMD,33,0*6D"); //semding commomd to turn anatana off in the GPS registers
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); //Set up a rate to 10Hz (10, 5, 1)
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); //saying we only want the sentances we want (RMC and GGA). 
  delay(1000);
}
//[1] ends here


int readGPS(){
  Serial.println("GPS function called");
  GPSresult = ""; //Reset the string SG
  //[2]
  while(!GPS.newNMEAreceived()){ //While there is no NMEA senstance
    c = GPS.read(); //read a char
  }
  GPS.parse(GPS.lastNMEA()); //pass the last senstance
  while(!GPS.newNMEAreceived()){ //While there is no NMEA senstance
    c = GPS.read(); //read a char
  }
  GPS.parse(GPS.lastNMEA()); //pass the last senstance
  while(!GPS.newNMEAreceived()){ //While there is no NMEA senstance
    c = GPS.read(); //read a char
  }
  GPS.parse(GPS.lastNMEA()); //pass the last senstance
  
  while(!GPS.newNMEAreceived()){ //While there is no NMEA senstance
    c = GPS.read(); //read a char
  }
  GPS.parse(GPS.lastNMEA()); //pass the last senstance
  NMEA1 = GPS.lastNMEA(); //First NMEA message equal to the last senstance

  while(!GPS.newNMEAreceived()){ //While there is no NMEA senstance
    c = GPS.read(); //read a char
  }
  GPS.parse(GPS.lastNMEA()); //pass the last senstance
  NMEA2 = GPS.lastNMEA(); //Second NMEA message equal to the last senstance

  Serial.print(NMEA1);
  Serial.println(NMEA2);

  if(GPS.fix == 1){ //only show data if there is a fix

    Serial.print(GPS.latitude,4); //pirnts the latitude to 4 decminal points
    Serial.print(GPS.lat); //prints the hemisphere
    Serial.print(",");
    Serial.print(GPS.longitude,4); //prints longitude
    Serial.print(GPS.lon);//prints Hemisphere
    Serial.print(",");
    Serial.println(GPS.altitude); //prints Altitude
    //[2] ends here
  }
}


/* Refances to the code used
 *  
 *  [1]P. McWhorter, LESSON 22: Build an Arduino GPS Tracker. United States: Paul McWhorter, 2014.
 *  https://www.youtube.com/watch?v=OsMoowoB2Rg
 *  
 *  [2]P. McWhorter, LESSON 23: Arduino GPS with Data Logger. United States: Paul McWhorter, 2014.
 *  https://www.youtube.com/watch?v=TdXbP8XhbX8
 *  
 *  [3]#47 - LIS3DH Accelerometer on an Arduino Pro Mini. United States: dotdissonance, 2020.
 *  https://www.youtube.com/watch?v=C09hG8OCBEk
 *  
 *  [4]Arduino-er. Unknown: Andr.oid Eric, 2016.
 *  http://arduino-er.blogspot.com/2016/04/blog-post.html
 */
