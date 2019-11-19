/*
  LED
  This example creates a BLE peripheral with service that contains a
  characteristic to control an LED.
  The circuit:
  - Arduino MKR WiFi 1010, Arduino Uno WiFi Rev2 board, Arduino Nano 33 IoT,
    Arduino Nano 33 BLE, or Arduino Nano 33 BLE Sense board.
  You can use a generic BLE central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.
  This example code is in the public domain.
*/

#include <ArduinoBLE.h>
#include <main.h>

BLEService ledService("5ffba521-2363-41da-92f5-46adc56b2d37"); // BLE LED Service

// BLE LED Switch Characteristic - custom 128-bit UUID, read and writable by central
// BLERead | BLEWrite remote clients will be able to get notifications if this characteristic changes
BLEByteCharacteristic switchCharacteristic("5ffba521-2363-41da-92f5-46adc56b2d37", BLERead | BLEWrite);

const int ledPin = LED_BUILTIN; // pin to use for the LED
const int dirPin = 2;
const int stepPin = 3;
const int stepsPerRevolution = 200;

void setup() {
  // Serial.begin(9600);
  // while (!Serial);

  // set LED pin to output mode
  pinMode(ledPin, OUTPUT);

  // Declare pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("LED");
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(switchCharacteristic);

  // add service
  BLE.addService(ledService);

  // set the initial value for the characeristic:
  switchCharacteristic.writeValue(0);

  // start advertising
  BLE.advertise();

  Serial.println("BLE LED Peripheral");
}

void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:
      if (switchCharacteristic.written()) {
        if (switchCharacteristic.value()) {   // any value other than 0
          Serial.println("LED on");
          rotateClockwise();
          digitalWrite(ledPin, HIGH);         // will turn the LED on
        } else {                              // a 0 value
          Serial.println(F("LED off"));
          rotateCClockwise();
          digitalWrite(ledPin, LOW);          // will turn the LED off
        }
      }
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}

void rotateClockwise() {
  digitalWrite(dirPin, HIGH);
  for(int x = 0; x < stepsPerRevolution; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(2000);
  }
}

void rotateCClockwise() {
  digitalWrite(dirPin, LOW);
  for(int x = 0; x < stepsPerRevolution; x++) {
  digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}
