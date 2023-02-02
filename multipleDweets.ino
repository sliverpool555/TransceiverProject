//Connecting array of data from sensors to a URL / IP Address
//The theroy of sending multiple sensor data over is from 
///dweet/for/sams?sensorA=23&sensorB=30&sensorC=40 https://www.youtube.com/watch?v=m-H4vz4HEp8

#include <ESP8266WiFi.h>

const int AnalogIn  = A0;
const int DigitalIn = D0; 

const char* ssid     = "VM213638";
const char* password = "acjwkxzMk4fp";

const char* host = "www.dweet.io";
const char* thing  = "group";
const char* thing_contentA = "SensorA";
const char* thing_contentB = "SensorB";

void setup() {
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void loop() {
  delay(1000);
  int valueA = analogRead(AnalogIn);
  int valueB = digitalRead(DigitalIn);

  Serial.print("connecting to ");
  Serial.println(host);
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
  // We now create a URI for the request
  String url = "/dweet/for/";
  url += thing;
  url += "?";
  url += thing_contentA;
  url += "=";
  url += valueA;
  url += "&";
  url += thing_contentB;
  url += "=";
  url += valueB;
  
  Serial.print("Requesting URL: ");
  Serial.println(url);
  
  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
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
}
