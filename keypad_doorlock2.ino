#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);  
#define Password_Length 5 

int signalPin = 23;
int flag = 0  ;
int count ;

char Data[Password_Length];
char Master[Password_Length] = "123A"; 
byte data_count = 0, master_count = 0;
bool Pass_is_good;
char customKey;
String doorStat = "Closed";

const byte ROWS = 4;
const byte COLS = 4;

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {32, 33, 27, 14};
byte colPins[COLS] = {16, 4, 2, 15};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);



void setup(){
  Serial.begin(9600);
  lcd.begin();                     
  lcd.backlight();
  pinMode(signalPin, OUTPUT);
  pinMode(35, INPUT);
  pinMode(34, INPUT);
  pinMode(17, OUTPUT);
  digitalWrite(signalPin, LOW);
  lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("SMART DOOR LOCK");
      lcd.setCursor(0,1); 
      lcd.print("      ");
      Serial.println("Correct");
}

void loop(){
  int x = digitalRead(35);
  int y = digitalRead(34);
  Serial.println("Enter Password:");
  lcd.setCursor(0, 0);
  lcd.print("Enter Password:");
  customKey = customKeypad.getKey();
  if (customKey){
    Data[data_count] = customKey; 
    lcd.setCursor(data_count,1); 
    lcd.print("*"); 
    data_count++; 
    }

  if(data_count == Password_Length-1){

    if(!strcmp(Data, Master)){
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
      if ((x == 0) && (flag ==0)){
      digitalWrite(signalPin, HIGH);
      lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(11,2); 
      lcd.print("Open");
      doorStat = "Open";
      Serial.println(doorStat); 
      flag =1;
      count = 0;
    delay(10000);
    lcd.clear();
      //digitalWrite(signalPin, LOW);
      }
      
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
      }
    clearData();  
  }
  if (count > 3 )
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
  if ((x == 0) && (flag ==1)){
    digitalWrite(signalPin, LOW);
    delay(1000);
    flag = 0;
      lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(11,2); 
      lcd.print("Closed      ");
    doorStat = "Closed";
  }
  if ((x == 1) && (flag ==0)){
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
  if (( x == 1) && ( flag ==1))
  {
    lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Door Stat:  ");
      lcd.setCursor(12,0); 
      lcd.print("Open  ");
      lcd.setCursor(0,1); 
      lcd.print("Enter Quickly!!! ");
      lcd.clear();
    
  }
  doorStat = "Closed";
  lcd.setCursor(0,2); 
      lcd.print("Door Stat:");
      lcd.setCursor(11,2); 
      lcd.print(doorStat);
  Serial.println(doorStat);
  delay(10);
  
}

void clearData(){
  while(data_count !=0){
    Data[data_count--] = 0; 
  }
  return;
}
