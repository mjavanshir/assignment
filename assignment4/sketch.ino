#include <ESP8266WiFi.h>   // برای ESP8266
#include <DHT.h>            // برای کار با سنسور دما

// تنظیمات WiFi
const char* ssid = "Your_SSID"; // نام شبکه Wi-Fi
const char* password = "Your_PASSWORD"; // پسورد Wi-Fi

// تنظیمات سرور (آدرس IP سرور یا آدرس URL)
const char* serverName = "http://your-server.com/upload"; // آدرس سرور

// تنظیمات سنسور دما
#define DHTPIN D2      // پین DATA سنسور دما
#define DHTTYPE DHT11  // نوع سنسور دما (DHT11 یا DHT22)
DHT dht(DHTPIN, DHTTYPE);

WiFiClient client;

void setup() {
  // put your setup code here, to run once:
// راه‌اندازی پورت سریال
  Serial.begin(115200);
  
  // اتصال به WiFi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
  
  // راه‌اندازی سنسور دما
  dht.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
 // خواندن دما و رطوبت
  float temperature = dht.readTemperature();  // دمای محیط
  float humidity = dht.readHumidity();        // رطوبت نسبی
  
  // چک کردن که آیا خواندن داده‌ها درست بوده
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  // چاپ دما و رطوبت در سریال مانیتور
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C, Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  // ارسال داده‌ها به سرور
  if (client.connect(serverName, 80)) {
    String postData = "temperature=" + String(temperature) + "&humidity=" + String(humidity);
    
    client.println("POST /upload HTTP/1.1");
    client.println("Host: your-server.com");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.print(postData);

    Serial.println("Data sent to server");
  } else {
    Serial.println("Failed to connect to server");
  }

  client.stop();
  
  // تاخیر قبل از ارسال دوباره
  delay(60000); // ارسال داده‌ها هر 60 ثانیه
}
