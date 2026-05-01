// Cod bariera fizica
#include <Wire.h>
#include <ESP32Servo.h>
#include <cctype>

#define trigPin 4
#define echoPin 5
#define servoPin 6
Servo servo;

float duration, distance;

bool isBarrierOpen = false;
int minTimeToClose = 7;
int minDistance = 10;

int command = 0;
int number = 0;
long timeOpened = 0;
int currentDistance = 100;

void setup() {
  // Ultrasonic sensor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  // Servo
  servo.setPeriodHertz(50);
  servo.attach(servoPin, 500, 2500);
  servo.write(0);
  // Serial
  Serial.begin(115200);
}

void loop() {
  command = 0;

  if (isBarrierOpen == true) readDistance(currentDistance);
  readSerial(command, number);

  switch(command) {
    case 0:
      break;
    case 1:
      getBarrierStatus();
      break;
    case 2:
      raiseBarrier();
      break;
    case 3:
      lowerBarrier();
      break;
    case 4:
      setTime();
      break;
  }
}

void getBarrierStatus() {
  Serial.print("1 ");
  Serial.println(isBarrierOpen);
}

void raiseBarrier() {
  if (isBarrierOpen == true) {
    Serial.println("2 0");
  }
  else {
    isBarrierOpen = true;
    timeOpened = millis()/1000;
    servo.write(90);
    Serial.println("2 1");
  }
}

void lowerBarrier() {
  long currentTime = millis()/1000;

  if (currentTime - timeOpened > minTimeToClose && currentDistance > minDistance) {
    timeOpened = 0;
    servo.write(0);
    isBarrierOpen = false;
    Serial.println("3 1");
  }
  else {
    Serial.println("3 0");
  }
}

void setTime() {
  minTimeToClose = number;
  Serial.print("Time set to: ");
  Serial.print(minTimeToClose);
  Serial.println(" s");
}

void readDistance(int& new_distance) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  new_distance = (duration*.0343)/2;
}

void readSerial(int& new_command, int& new_number) {
  char inputChar;

  if (Serial.available() > 0) {
    inputChar = Serial.read();

    if (isdigit(inputChar)) {
      int temp = int(inputChar - '0');
      
      if (temp >= 1 && temp <= 4) {
        new_command = temp;

        if (new_command == 4) {
          bool end = false;
          char number_char[16];
          int i = 0;
          while (Serial.available() > 0 && end == false) {
            inputChar = Serial.read();
            if (inputChar != ' ' && inputChar != '\n') {
              number_char[i] = inputChar;
              i++;
            }
            else if (inputChar == '\n') {
              end = true;
            }
          }

          sscanf(number_char, "%d", &new_number);
        }

      }
      else {
        new_command = 0;
      }

    }
    else {
      new_command = 0;
    }

  }
  else {
    new_command = 0;
  }
}