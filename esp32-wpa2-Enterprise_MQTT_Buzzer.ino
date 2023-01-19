
#include <WiFi.h> //Wifi library
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks
#define EAP_IDENTITY "50058" //if connecting from another corporation, use identity@organisation.domain in Eduroam 
#define EAP_PASSWORD "Jada@@6228" //your Eduroam password
const char* ssid = "KIIT-WIFI-NET."; // Eduroam SSID
const char* host = "arduino.php5.sk"; //external server domain for HTTP connection after authentification

int counter = 0;
int BuzIP;
#include <PubSubClient.h>
#define LedPin 5
#define buzPin 4
WiFiClient espClient;
PubSubClient client(espClient);

long now = millis();
long lastMeasure = 0;

const char* mqtt_server = "10.0.2.19";

// NOTE: For some systems, various certification keys are required to connect to the wifi system.
//       Usually you are provided these by the IT department of your organization when certs are required
//       and you can't connect with just an identity and password.
//       Most eduroam setups we have seen do not require this level of authentication, but you should contact
//       your IT department to verify.
//       You should uncomment these and populate with the contents of the files if this is required for your scenario (See Example 2 and Example 3 below).
//const char *ca_pem = "insert your CA cert from your .pem file here";
//const char *client_cert = "insert your client cert from your .crt file here";
//const char *client_key = "insert your client key from your .key file here";

void setup() {
  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.print("Connecting to network: ");
  Serial.println(ssid);
  WiFi.disconnect(true);  //disconnect form wifi to set new wifi connection
  WiFi.mode(WIFI_STA); //init wifi mode
 
//   Example1 (most common): a cert-file-free eduroam// with PEAP (or TTLS)
//  WiFi.begin(ssid);/

  // Example 2: a cert-file WPA2 Enterprise with PEAP
  WiFi.begin(ssid, WPA2_AUTH_PEAP, EAP_IDENTITY, EAP_USERNAME, EAP_PASSWORD, ca_pem, client_cert, client_key);
 
  // Example 3: TLS with cert-files and no password
  //WiFi.begin(ssid, WPA2_AUTH_TLS, EAP_IDENTITY, NULL, NULL, ca_pem, client_cert, client_key);
 
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    counter++;
    if(counter>=60){ //after 30 seconds timeout - reset board
      ESP.restart();
    }
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address set: ");
  Serial.println(WiFi.localIP()); //print LAN IP
  client.setServer(mqtt_server, 1887);
  client.setCallback(callback);
//  BuzIP = (int)WiFi.localIP() ;
  

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    /*CHANGE IF connecting MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, will have to give a new name to the ESP8266.  */
    if (client.connect("Campus20")) {
      Serial.println("connected");  
//      client.subscribe("678569/approval_status");
//      client.subscribe("678569/destination");
//      client.subscribe("2714273/movement");
        client.subscribe("678569/status");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) { //if we are connected to Eduroam network
    counter = 0; //reset counter
    Serial.println("Wifi is still connected with IP: ");
    Serial.println(WiFi.localIP());   //inform user about his IP address
  }else if (WiFi.status() != WL_CONNECTED) { //if we lost connection, retry
    WiFi.begin(ssid);      
  }
  while (WiFi.status() != WL_CONNECTED) { //during lost connection, print dots
    delay(500);
    Serial.print(".");
    counter++;
    if(counter>=60){ //30 seconds timeout - reset board
    ESP.restart();
    }
  }
   if (!client.connected()) {
    reconnect();
  }
 
  if(!client.loop())
    client.connect("Campus20");

  now = millis();
}
void callback(String topic, byte* message, unsigned int length) {

  byte* p = (byte*)malloc(length);
  // Copy the payload to the new buffer
  memcpy(p,message,length);
  client.publish("ackno", p, length);
  free(p);
  
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.println(". Message: ");
  String messageTemp;
 
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if(topic == "ackno" ){
    client.publish("ackno",(const char*)BuzIP);
  }
  
  if(topic == "678569/status"){
    Serial.println("Alert State : ");
     if (messageTemp == "Unauthorized"){
      digitalWrite(23,1);
      delay(3000);
      Serial.print("Active");
      digitalWrite(23,0);
     }
     if (messageTemp == "Not approved"){
      digitalWrite(23,1);
      delay(3000);
      Serial.print("Active");
      digitalWrite(23,0);
     }    
    }
    if (messageTemp == "Wrong Destination"){
      digitalWrite(23,1);
      delay(3000);
      Serial.print("Active");
      digitalWrite(23,0);
      }
      if (messageTemp == "Approved"){
      digitalWrite(23,0);      
    }
    if (messageTemp == "Entry point"){
      digitalWrite(23,0);      
    }
     else{
      digitalWrite(23,0);
      }
    Serial.println();
  }
