#include <Arduino.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "SPIFFS.h"
#include "index.h"

#define ROTEADOR 

#define pinLA 14
#define pinLB 27
#define pinLPWM 19
#define pinRA 26
#define pinRB 25
#define pinRPWM 23

#ifdef ROTEADOR
// const char* ssid = "Allicia30";
// const char* password = "123aaa123";
// const char* ssid = "TesteRobotics";
// const char* password = "RoboTQ9812w";
// const char* ssid = "ws_iot";
// const char* password = "Us0C0nc1enT3";
// const char* ssid = "Casa_Wifi2";
// const char* password = "@r1@n3mr";
const char* ssid = "Familia Santos-2.4G";
const char* password = "teste1234";
#else
const char* ssid = "ESP_Car";
const char* password = "carro123";
#endif

AsyncWebServer server(80);
AsyncEventSource events("/events");

Adafruit_MPU6050 mpu;

bool isLogging = false;
unsigned long startTime = 0;  

String dataBuffer = "";   
const int batchSize = 10; 
int bufferCount = 0;      

void motorStop() {
  digitalWrite(pinLA, LOW);
  digitalWrite(pinLB, LOW);
  digitalWrite(pinRA, LOW);
  digitalWrite(pinRB, LOW);
}

void motorForward() {
  digitalWrite(pinLA, LOW);
  digitalWrite(pinLB, HIGH);
  digitalWrite(pinRA, LOW);
  digitalWrite(pinRB, HIGH);
}

void motorBack() {
  digitalWrite(pinLA, HIGH);
  digitalWrite(pinLB, LOW);
  digitalWrite(pinRA, HIGH);
  digitalWrite(pinRB, LOW);
}

void motorLeft() {
  digitalWrite(pinLA, HIGH);
  digitalWrite(pinLB, LOW);
  digitalWrite(pinRA, LOW);
  digitalWrite(pinRB, HIGH);
}

void motorRight() {
  digitalWrite(pinLA, LOW);
  digitalWrite(pinLB, HIGH);
  digitalWrite(pinRA, HIGH);
  digitalWrite(pinRB, LOW);
}

void setup() {
  Serial.begin(115200);

  // Inicializa SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("Erro ao montar SPIFFS!");
    return;
  }

  // Inicializa Wi-Fi
#ifdef ROTEADOR
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConectado!");
  Serial.print("IP do servidor: ");
  Serial.println(WiFi.localIP());
#else
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("IP do servidor: ");
  Serial.println(IP);
#endif

  // Inicializa I2C para o MPU6050
  Wire.begin(21, 22);
  if (!mpu.begin()) {
    Serial.println("Falha ao inicializar o MPU6050!");
    while (1) delay(10);
  }
  Serial.println("MPU6050 pronto!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Pinos do robô
  pinMode(pinLA, OUTPUT);
  pinMode(pinLB, OUTPUT);
  pinMode(pinLPWM, OUTPUT);
  pinMode(pinRA, OUTPUT);
  pinMode(pinRB, OUTPUT);
  pinMode(pinRPWM, OUTPUT);

  analogWrite(pinLPWM, 120);
  analogWrite(pinRPWM, 120);

  motorStop();

  // Serve arquivos estáticos (CSS, etc.)
  server.serveStatic("/", SPIFFS, "/");

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", INDEX_HTML);
  });

  server.on("/datalog", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/datalog.txt", "text/plain", true);
  });

  server.on("/startlog", HTTP_GET, [](AsyncWebServerRequest *request){
    isLogging = true;
    startTime = millis();  // Zera o tempo base aqui
    File file = SPIFFS.open("/datalog.txt", FILE_WRITE);
    if (file) {
      file.println("timestamp, accX, accY, accZ, gyroX, gyroY, gyroZ");
      file.close();
    }
    request->send(200, "text/plain", "Logger iniciado.");
  });

  server.on("/stoplog", HTTP_GET, [](AsyncWebServerRequest *request){
    if (dataBuffer.length() > 0) {
      File file = SPIFFS.open("/datalog.txt", FILE_APPEND);
      if (file) {
        file.print(dataBuffer);
        file.close();
      }
      dataBuffer = "";
      bufferCount = 0;
    }

    isLogging = false;
    request->send(200, "text/plain", "Logger parado.");
  });

  // Comandos do robô
  server.on("/f", HTTP_GET, [](AsyncWebServerRequest *request){
    motorForward();
    request->send(200, "text/plain", "Frente");
  });

  server.on("/b", HTTP_GET, [](AsyncWebServerRequest *request){
    motorBack();
    request->send(200, "text/plain", "Trás");
  });

  server.on("/l", HTTP_GET, [](AsyncWebServerRequest *request){
    motorLeft();
    request->send(200, "text/plain", "Esquerda");
  });

  server.on("/r", HTTP_GET, [](AsyncWebServerRequest *request){
    motorRight();
    request->send(200, "text/plain", "Direita");
  });

  server.on("/s", HTTP_GET, [](AsyncWebServerRequest *request){
    motorStop();
    request->send(200, "text/plain", "Parar");
  });

  events.onConnect([](AsyncEventSourceClient *client){
    client->send("hello!", NULL, millis(), 1000);
  });
  server.addHandler(&events);

  server.begin();
}

unsigned long lastReadTime = 0;
const unsigned long readInterval = 100;

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastReadTime >= readInterval) {
    lastReadTime = currentTime;

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    String json = "{";
    json += "\"accX\":" + String(a.acceleration.x, 2) + ",";
    json += "\"accY\":" + String(a.acceleration.y, 2) + ",";
    json += "\"accZ\":" + String(a.acceleration.z, 2) + ",";
    json += "\"gyroX\":" + String(g.gyro.x, 2) + ",";
    json += "\"gyroY\":" + String(g.gyro.y, 2) + ",";
    json += "\"gyroZ\":" + String(g.gyro.z, 2);
    json += "}";

    events.send(json.c_str(), "sensor_readings", millis());

    if (isLogging) {
      unsigned long timestamp = millis() - startTime;

      String line = String(timestamp) + ", " +
                    String(a.acceleration.x, 2) + ", " +
                    String(a.acceleration.y, 2) + ", " +
                    String(a.acceleration.z, 2) + ", " +
                    String(g.gyro.x, 2) + ", " +
                    String(g.gyro.y, 2) + ", " +
                    String(g.gyro.z, 2) + "\n";

      dataBuffer += line;
      bufferCount++;

      if (bufferCount >= batchSize) {
        File file = SPIFFS.open("/datalog.txt", FILE_APPEND);
        if (file) {
          file.print(dataBuffer);
          file.close();
        }
        dataBuffer = "";
        bufferCount = 0;
      }
    }
  }
}
