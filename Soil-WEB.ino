#include <WiFi.h>
#include <HTTPClient.h>

// Pin configurations
int sensor_pin = 2;  // Analog pin for moisture sensor, change based on your setup
int moisture, sensor_analog;

const char* ssid = "Huawei Y7";
const char* password = "tyr567hi";
const char* serverName = "http://192.168.43.162:5000/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Wait for WiFi connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Read and calculate moisture level
    sensor_analog = analogRead(sensor_pin);
    moisture = (100 - ((sensor_analog / 4095.00) * 100));
    Serial.print("Moisture = ");
    Serial.print(moisture); 
    Serial.println("%");

    // Check soil moisture level
    if (moisture < 30) {
      Serial.println("Soil is dry");
    } else {
      Serial.println("Soil is wet or moist");
    }

    // Send data to the Flask server
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"Moisture\":" + String(moisture) + "}";
    int httpResponseCode = http.POST(jsonData);

    // Check server response
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
  
  delay(10000);  // Send data every 10 seconds
}
