#include <WiFi.h>
#include <PubSubClient.h>
#include "credentials.h"

#define LedPin 2
#define buzPin 13
//#define MQTTsubQos 1


WiFiClient espClient;
PubSubClient client(espClient);

long now = millis();
long lastMeasure = 0;

const char* mqtt_server = "20.205.208.135";

void config_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf(" location : %s ;", location);
  Serial.printf("Device ID : %s ", deviceID);
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    /*CHANGE IF connecting MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, will have to give a new name to the ESP8266.  */
    if (client.connect("P.S.")) {
      Serial.println("connected");  

//      client.subscribe("topic");
        client.subscribe(topic1Alert.c_str());
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(buzPin, OUTPUT);
 
  Serial.begin(115200);
  config_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}



void callback(String Topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(Topic);
  Serial.println(". Message: ");
  String messageTemp;
 
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if(Topic == topic1Alert){
    Serial.println(Topic);

  if (messageTemp == "theft/alarm_on"){
    digitalWrite(buzPin,1);
    Serial.println("Alarm is on");
//    delay(2000);

  }
  if (messageTemp == "theft/alarm_off"){
   digitalWrite(buzPin,0);  
  }
  }

  if(Topic == ""){
    Serial.println(Topic);

  if (messageTemp == "Theft")
    digitalWrite(buzPin,1);
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  
  if(!client.loop())
    client.connect("P.S.");

  now = millis();
} 
