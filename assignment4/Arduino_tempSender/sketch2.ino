#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SSID";        // نام شبکه WiFi
const char* password = "PASSWORD"; // رمز عبور WiFi

const char* serverName = "http://your-server.com/endpoint"; // URL سرور

void setup() {
  Serial.begin(115200); // شروع ارتباط سریال
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // دریافت داده‌ها از Arduino

    // ارسال داده‌ها به سرور
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      String jsonData = "{\"data\": \"" + data + "\"}";
      int httpResponseCode = http.POST(jsonData);

      if (httpResponseCode > 0) {
        Serial.println("Data sent successfully");
        Serial.println(httpResponseCode);
      } else {
        Serial.println("Error in sending data");
      }
      http.end();
    } else {
      Serial.println("WiFi Disconnected");
    }
  }

  delay(1000); // خواندن داده‌ها هر 1 ثانیه
}
