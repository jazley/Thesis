#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <ESP8266WiFi.h>

const char* ssid = "NETWORK_SSID";
const char* password = "NETWORK_PASSWORD";
const char* host = "NETWORK_IP_ADDRESS";
const int port = 8888;

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345); // Change the I2C address if necessary
WiFiClient client;

unsigned long previousMillis = 0;
const long interval = 500; // Interval at which to send data (in milliseconds)

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (!mag.begin()) {
    Serial.println("Could not find a valid HMC5883 sensor, check wiring!");
    while (1);
  }

  delay(1000);
  Serial.println("Connecting to WiFi network...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (!client.connected()) {
      Serial.println("Connecting to server...");
      if (client.connect(host, port)) {
        Serial.println("Connected to server");
      } else {
        Serial.println("Unable to connect to server");
        return;
      }
    }

    sensors_event_t event;
    mag.getEvent(&event);

    float x = event.magnetic.x;
    float y = event.magnetic.y;
    float z = event.magnetic.z;

    String data = String(x) + "," + String(y) + "," + String(z);
    client.print(data);

    delay(10);  // Add a small delay to allow data to be sent in chunks
  }
}
