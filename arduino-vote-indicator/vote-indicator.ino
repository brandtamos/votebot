#include <Servo.h>
#include <SoftwareSerial.h>

const int MINSERVOPOS = 0;
const int MAXSERVOPOS = 200;
const int SERVOPIN = 9;

Servo myservo;
int servopos = MINSERVOPOS;
float voteValue = 0.5;
float oldVoteValue = voteValue;
String serialString;

void setup() {
  Serial.begin(9600);
  myservo.attach(SERVOPIN);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    serialString = Serial.readString();
    voteValue = serialString.toFloat();
    if(voteValue != oldVoteValue){
      actuateServo(voteValue);
      oldVoteValue = voteValue;
    }
    
  }
}

void setServoToStartPosition(){
  pinMode(SERVOPIN, OUTPUT);
  
  myservo.write(MINSERVOPOS);              // tell servo to go to position in variable 'pos'
  delay(200);                       // waits 15ms for the servo to reach the position
  pinMode(SERVOPIN, INPUT);
}

void actuateServo(float voteValue){
  pinMode(SERVOPIN, OUTPUT);
  servopos = (int)(voteValue * MAXSERVOPOS);
  myservo.write(servopos);              // tell servo to go to position in variable 'pos'
  delay(500);                       // waits 15ms for the servo to reach the position
  pinMode(SERVOPIN, INPUT);
}

