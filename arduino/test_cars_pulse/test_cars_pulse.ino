#include <Arduino.h>
#include <ArduinoJson.h>

void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0));
}

void loop() {
  StaticJsonDocument<250> doc;

  // Data ban
  for(int i=1;i<=4;i++){
    doc[String("ban") + i] = random(28, 36);           // PSI
    doc[String("status") + i] = (random(0,2) == 0 ? "OK" : "WARNING"); // status per ban
  }

  // GPS
  doc["lat"] =  -6.2 + (random(0,100)/1000.0);  
  doc["lon"] = 106.8 + (random(0,100)/1000.0);  

  serializeJson(doc, Serial);
  Serial.println();

  delay(1000);
}
