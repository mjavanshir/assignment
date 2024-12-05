#include <DHT.h>

#define DHTPIN 4        // پین متصل به سنسور DHT22
#define DHTTYPE DHT22   // نوع سنسور (DHT22)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); // شروع ارتباط سریال
  dht.begin();        // راه‌اندازی سنسور DHT22
}

void loop() {
  // خواندن داده‌ها از سنسور
  float temperature = dht.readTemperature(); // دما
  float humidity = dht.readHumidity();       // رطوبت

  // چک کردن صحت داده‌ها
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // ارسال داده‌ها از طریق پورت سریال به ESP8266 یا ESP32
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  delay(2000); // خواندن هر 2 ثانیه
}
