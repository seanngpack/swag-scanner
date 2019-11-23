/*
  main.cpp
  This file sets up bluetooth capabilities and defines functions for rotating
  the a stepper motor using the AccelStepper library
  The circuit:
  - Arduino Nano 33 IoT, DRV8825 driver, Nema 17 17HS08-1004S (18.4oz-in) stepper,
  You can use a generic BLE central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.
*/

#include <ArduinoBLE.h>
#include <main.h>
#include <math.h>
#include <AccelStepper.h>

// Scanner Service
// custom 128-bit UUID
BLEService scannerService("5ffba521-2363-41da-92f5-46adc56b2d37"); 

// BLE Scanner characterisic - custom 128-bit UUID, read and writable by central
// BLERead | BLEWrite remote clients will be able to read & write
BLEByteCharacteristic rotateTableCharacteristic("5ffba521-2363-41da-92f5-46adc56b2d37", BLERead | BLEWrite);

// BLE Scanner characterisic - custom 128-bit UUID, read and writable by central
// BLERead | BLENotify remote clients will be able to get notifications if this characteristic changes
BLEByteCharacteristic tablePositionCharacteristic("5ffba523-2363-41da-92f5-46adc56b2d37", BLERead | BLENotify);

const int ledPin = LED_BUILTIN; // use built-in LED
const int motorInterfaceType = 1;
const int dirPin = 2;
const int stepPin = 3;
const int sleepPin = 4;
const int gearRatio = 60;
const int stepsPerRev = 200;
const float degPerStep = 360.0/float(stepsPerRev * gearRatio);
const int motorSpeed = 100;

// create new instance of stepper motor
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup()
{
  Serial.begin(9600);

  // set built-in LED pin to output mode
  pinMode(ledPin, OUTPUT);

  // Declare pins as Outputs
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(sleepPin, OUTPUT);
  
  // set initial values for the stepper
  stepper.setMaxSpeed(500);
  stepper.setCurrentPosition(0);

  // begin BLE initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("SwagScanner");
  BLE.setAdvertisedService(scannerService);

  // add characteristics to the service
  scannerService.addCharacteristic(rotateTableCharacteristic);
  scannerService.addCharacteristic(tablePositionCharacteristic);

  // add service
  BLE.addService(scannerService);

  // set the initial value for the characeristic:
  rotateTableCharacteristic.writeValue(0);

  // start advertising
  BLE.advertise();
  Serial.println("BLE initialized, waiting for connection...");
}

void loop()
{
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central)
  {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());
    digitalWrite(ledPin, HIGH); // will turn the LED on
    // while the central is still connected to peripheral:
    while (central.connected())
    {
      // if the remote device wrote to the characteristic,
      // use the value to control the stepper:
      if (rotateTableCharacteristic.written())
      {
        int value = rotateTableCharacteristic.value();
        if (value)
        { 
          Serial.println(value);
          // rotate the table based on input!
          rotateTable(value);
        }
        else
        {
          Serial.println("0 entered for the bed rotation, why would you do that?");
        }
      }
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}

// 1 = in progress, 0 = done
void rotateTable(int degs)
{
  // rotateTableCharacteristic.setValue(1);
  // calculate the # of steps to rotate
  long steps = degToSteps(degs);
  long nextStepperPosition = stepper.currentPosition() + steps;
  Serial.println((String)"next position at:" + nextStepperPosition);

  Serial.println((String)"table position before: "  + getTablePosition());

  // set the stepper to rotate CW 
  if (steps > 0) {
    stepper.setSpeed(motorSpeed);
  }
  // set the stepper to rotate CW 
  else 
  {
    stepper.setSpeed(-motorSpeed);
  }

  while(stepper.currentPosition() != nextStepperPosition) 
  {
    // Serial.println(stepper.currentPosition());
    stepper.runSpeed();
  }
  // rotateTableCharacteristic.setValue(0);
  Serial.print((String)"finished rotating the stepper... " + stepper.currentPosition());

  Serial.println((String)"table position after: " + getTablePosition());
}

// convert the BLE input of degrees to # of steps for the stepper to move
// BE CAREFUL OF INPUT, floats gets downcasted to longs and there's precision
// loss for non increments of the degPerStep constant
long degToSteps(int degs)
{
  if (fmod(float(degs), degPerStep) != 0.0)
  {
    Serial.println("WARNING, precision loss bout to happen");
  }
  Serial.println((String)"Here are the number of degrees we want to rotate to: " + degs);
  
  long steps = degs/degPerStep;
  Serial.println((String)"Here are the steps" + steps);
  return steps;
}

// get the current position of the table away from home (0 deg) in degrees
long getTablePosition()
{
  long tablePosition = fmod(((float)(stepper.currentPosition()) * degPerStep), 360.0);
  Serial.println((String)"this is the current table position" + tablePosition);
  tablePositionCharacteristic.setValue(tablePosition);
  return tablePosition;
}