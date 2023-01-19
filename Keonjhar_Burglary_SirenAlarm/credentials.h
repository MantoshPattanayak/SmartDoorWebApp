const char* ssid = "LORA";
const char* password = "62329262";

String location = "KUNDALAI HIGH SCHOOL";
String locationID = "1";
String deviceID = "9";
String Mestype1 = "Set_Alert";
String Mestype2 = "getstatus";

                     //Alarm001/SchoolID/Schoolname/SetAlert
String topic1Alert = deviceID+"/"+locationID+"/"+location+"/"+Mestype1;

//String topic1Alert = "9/1/KUNDALAI HIGH SCHOOL/Set_Alert";

String topic2 = "";
