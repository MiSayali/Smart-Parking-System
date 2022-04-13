#include <BoltIoT-Arduino-Helper.h>
#define echoPin 8 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 9 //attach pin D3 Arduino to pin Trig of HC-SR04
double duration;
int distance;

void setup(){
  boltiot.begin(Serial);
  boltiot.setCommandString("getReading", getReading);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
}

String getReading(){
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  digitalWrite(LED_BUILTIN, HIGH);  

  return String(distance);
}

void loop(){
  boltiot.handleCommand();
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);  
}
