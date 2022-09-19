#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>


/* User Defined Parameters ------------------------*/
double samp_freq = 60.0;      // Hz
/*-------------------------------------------------*/


// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

unsigned long count = 0;    // last discrete time
unsigned long n = count;    // discrete time
unsigned long start_millis; // starting continuous time
unsigned long t;            // continuous time

int emg1, emg2, emg3, emg4;

void setup(void)
{
  Serial.begin(115200);

  if (!bno.begin()) {
    Serial.print("No BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  pinMode(A8, INPUT);
  pinMode(A9, INPUT);
  pinMode(A10, INPUT);
  pinMode(A11, INPUT);
  
  delay(1000);
  start_millis = millis();
}


void loop(void){
  /* Wait */
  while(1){
    t = millis() - start_millis;
    n = int(t / 1000.0 * samp_freq);
    if (n > count){
      count += 1;
      break;
    }
  }
  
  /* Data Acquisition */
  sensors_event_t orientationData , angVelocityData , linearAccelData, magnetometerData, accelerometerData, gravityData;
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);
  emg1 = analogRead(A8);
  emg2 = analogRead(A9);
  emg3 = analogRead(A10);
  emg4 = analogRead(A11);

  /* Data Printing */
  Serial.print(n);
  Serial.print("\t");
  Serial.print(emg1);
  Serial.print("\t");
  Serial.print(emg2);
  Serial.print("\t");
  Serial.print(emg3);
  Serial.print("\t");
  Serial.print(emg4);
  Serial.print("\t");
  printEvent(&angVelocityData);
  printEvent(&linearAccelData);
  Serial.println();

  /* 乱七八糟的代码 */
//  samp_freq += 0.1;
//  if ((n - count) != 1){
//    Serial.print("Lag!! Sampling frequency = ");
//    Serial.print(samp_freq);
//    while(1);
//  }
//  count++;
}


void printEvent(sensors_event_t* event) {
  double x = -1000000, y = -1000000 , z = -1000000; //dumb values, easy to spot problem
  if (event->type == SENSOR_TYPE_ACCELEROMETER) {
//    Serial.print("Accl:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else if (event->type == SENSOR_TYPE_ORIENTATION) {
//    Serial.print("Orient:");
    x = event->orientation.x;
    y = event->orientation.y;
    z = event->orientation.z;
  }
  else if (event->type == SENSOR_TYPE_MAGNETIC_FIELD) {
//    Serial.print("Mag:");
    x = event->magnetic.x;
    y = event->magnetic.y;
    z = event->magnetic.z;
  }
  else if (event->type == SENSOR_TYPE_GYROSCOPE) {
//    Serial.print("Gyro:");
    x = event->gyro.x;
    y = event->gyro.y;
    z = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_ROTATION_VECTOR) {
//    Serial.print("Rot:");
    x = event->gyro.x;
    y = event->gyro.y;
    z = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_LINEAR_ACCELERATION) {
//    Serial.print("Linear:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else if (event->type == SENSOR_TYPE_GRAVITY) {
//    Serial.print("Gravity:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else {
//    Serial.print("Unk:");
  }

  Serial.print(x);
  Serial.print("\t");
  Serial.print(y);
  Serial.print("\t");
  Serial.print(z);
  Serial.print("\t");
}
