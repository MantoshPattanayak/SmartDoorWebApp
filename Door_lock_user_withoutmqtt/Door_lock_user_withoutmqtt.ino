#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);  

int signalPin = 23;

#define P_Lenght 6 // Give enough room for six chars + NULL char
#define U_Lenght 5

char Data1[P_Lenght]; // 6 is the number of chars it can hold + the null char = 7
char Data[U_Lenght];
char Master1[P_Lenght] = "9852A";
char Master[U_Lenght] = "7102";

byte data_count = 0, master_count = 0;

//bool Pass_is_good;

char customKey;

const byte ROWS = 4;

const byte COLS = 4;

char hexakeys[ROWS][COLS] = {

  {'1', '2', '3','A'},

  {'4', '5', '6','B'},

  {'7', '8', '9','C'},

  {'*', '0', '#','D'}

};
int us = 0;
int door = 1;
int count = 0;
String doorStat = "Closed";
byte rowPins[ROWS] = {32, 33, 27, 14}; //connect to the row pinouts of the keypad

byte colPins[COLS] = {16, 4, 2, 15}; //connect to the column pinouts of the keypad

Keypad customKeypad = Keypad( makeKeymap(hexakeys), rowPins, colPins, ROWS, COLS); //initialize an instance of class NewKeypad



void setup()

{

  Serial.begin(9600);
  lcd.begin();                     
  lcd.backlight();
  pinMode(signalPin, OUTPUT);
  pinMode(35, INPUT);
  pinMode(18, INPUT);
  pinMode(17, OUTPUT);
  digitalWrite(signalPin, LOW);
  lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("SMART DOOR LOCK");
      lcd.setCursor(0,2); 
      lcd.print("Developed By:");
      lcd.setCursor(0,3); 
      lcd.print("!!!! SOUL IOT !!!!!");
      delay(3000);
lcd.clear();     
}

void loop()

{
  delay(100);
  int x = digitalRead(35);
  int y = digitalRead(18);
  if (door == 0)

  {

    customKey = customKeypad.getKey();

    if (x == 0)

    {
      delay(1000);
      digitalWrite(signalPin, LOW);
      /*lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(11,2); 
      lcd.print("Closed      ");*/
    doorStat = "Closed";
      lcd.clear();
      door = 1;
      us = 0;

    }
    else
    {
      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Door Stat:  ");
      lcd.setCursor(0,1); 
      lcd.print(doorStat);
      lcd.setCursor(0,2); 
      lcd.print(" Close the door");
      lcd.setCursor(0,3); 
      lcd.print(" Thank You!!!");
      delay(1000);
      lcd.clear();
    }

  }
  //int x = digitalRead(35);
  
  if((door == 1) && (x ==0) && (us == 0))
  {
    user_valid();
  }
  if((door == 1) && (x ==0) && (us == 1))
  {
    pass_Open();
  }
  if ((door == 1) && (x ==1))
  {
    doorStat = "Forced Entry";
    lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Door Stat:  ");
      lcd.setCursor(0,1); 
      lcd.print("Forced Entry!!!  ");
      lcd.setCursor(0,2); 
      lcd.print("Contact Police      ");
    Serial.println(doorStat);
    digitalWrite(17, HIGH);
    delay(1000);
    digitalWrite(17, LOW);
    delay(100);
    digitalWrite(17, HIGH);
    delay(1500);
    digitalWrite(17, LOW);
    delay(3000);
    lcd.clear();
  }
  if(count > 3)
  {
    doorStat = "Invalid_User";
      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Password Stat:");
      lcd.setCursor(0,1); 
      lcd.print("Multiple Wrong Entry      ");
      lcd.setCursor(0,2); 
      lcd.print("Contact Authority");
      lcd.setCursor(0,3); 
      lcd.print("For Access");
    Serial.println(doorStat);
    digitalWrite(17, HIGH);
    delay(1000);
    digitalWrite(17, LOW);
    delay(100);
    digitalWrite(17, HIGH);
    delay(1500);
    digitalWrite(17, LOW);
    delay(50);
  }
  if(y == 1)
  {
    digitalWrite(signalPin, HIGH);
    doorStat = "Opened";
      lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(0,3); 
      lcd.print(doorStat);
      delay(3000);
      door = 0;
  }
   lcd.setCursor(0,2);
lcd.print("Door Stat:");
      lcd.setCursor(0,3); 
      lcd.print(doorStat);
}

void clearData()

{

  while (data_count != 0)

  { // This can be used for any array size,

    Data[data_count--] = 0; //clear array for new data

  }

  return;

}
void clearData1()

{

  while (data_count != 0)

  { // This can be used for any array size,

    Data1[data_count--] = 0; //clear array for new data

  }

  return;

}

void pass_Open()

{
  //lcd.clear();

  lcd.setCursor(0, 0);

  lcd.print("Enter Password");

  customKey = customKeypad.getKey();

  if (customKey) // makes sure a key is actually pressed, equal to (customKey != NO_KEY)

  {

    Data1[data_count] = customKey; // store char into data array

    lcd.setCursor(data_count, 1); // move cursor to show each new char

    lcd.print('*'); // print char at said cursor

    data_count++; // increment data array by 1 to store new char, also keep track of the number of chars entered

  }

  if (data_count == P_Lenght - 1) // if the array index is equal to the number of expected chars, compare data to master

  {

    if (!strcmp(Data1, Master1)) // equal to (strcmp(Data, Master) == 0)

    {

      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Password Stat:");
      lcd.setCursor(0,1); 
      lcd.print("    Correct      ");
      Serial.println("Correct");
    digitalWrite(17, HIGH);
    delay(100);
    digitalWrite(17, LOW);
    delay(50);
    digitalWrite(17, HIGH);
    delay(250);
    digitalWrite(17, LOW);
    delay(50);
    digitalWrite(signalPin, HIGH);
      /*lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(11,2); 
      lcd.print("Open");*/
      doorStat = "Open";
      lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(0,3); 
      lcd.print(doorStat);
      delay(5000);
      door = 0;
      us = 0;
      clearData1();
      lcd.clear();
    }
    else{

      Serial.println("Incorrect");
      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Password Stat:");
      lcd.setCursor(0,1); 
      lcd.print(" !!!Incorrect!!!      ");
      digitalWrite(17, HIGH);
      delay(500);
      digitalWrite(17, LOW);
      delay(150);
      digitalWrite(17, HIGH);
      delay(750);
      digitalWrite(17, LOW);
      delay(2000);
      count ++;
      lcd.clear();
      clearData1();
      door = 1;
      us = 0;

    }
    
  }

    

  }

void user_valid()

{

  lcd.setCursor(0, 0);

  lcd.print(" Enter User");

  customKey = customKeypad.getKey();

  if (customKey ) // makes sure a key is actually pressed, equal to (customKey != NO_KEY)

  {

    Data[data_count] = customKey; // store char into data array

    lcd.setCursor(data_count, 1); // move cursor to show each new char

    lcd.print(Data[data_count]); // print char at said cursor

    data_count++; // increment data array by 1 to store new char, also keep track of the number of chars entered

  }

  if (data_count == U_Lenght-1) // if the array index is equal to the number of expected chars, compare data to master

  {

    if (!strcmp(Data, Master)) // equal to (strcmp(Data, Master) == 0)

    {

      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("User Stat:");
      lcd.setCursor(0,1); 
      lcd.print("    Correct      ");
      delay(2000);
      Serial.println("Correct");
      clearData();
      lcd.clear();
      us = 1;

    }
    else{

      Serial.println("Incorrect");
      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("User Stat:");
      lcd.setCursor(0,1); 
      lcd.print(" !!!Incorrect!!!      ");
      delay(2000);
      lcd.clear();
      clearData();
      us = 0;
    }
   
    
  }

    

  }



