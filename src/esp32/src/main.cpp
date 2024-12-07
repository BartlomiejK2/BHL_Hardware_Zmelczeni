#include <Arduino.h>

void setup() {
  Serial.begin(115200); 
  Serial2.begin(9600, SERIAL_8N1, 16, 17); // uruchomienie RX2 i TX2 odpowiednio
}
void loop() {
  
  float sensor_volt; // napięcie na czujnikuj gazu
  float RS_gas; // Get value of RS in a GAS
  float ratio; // Get ratio RS_GAS/RS_air
  float pulse_volt;// napięcie z czujnika pulsu
  int sensorValue = analogRead(4);//pind4 analog czujnik gazu
  int sensorValue2= analogRead(33);//pin33 analog czujnik pulsu
  pulse_volt=(float)sensorValue2/4095*100.0; //przeksztalcenie na % wartosci "pulsu"
  sensor_volt=(float)sensorValue/1024*5.0; // przeksztalcenie na napiecie do wzorku
  RS_gas = (5.0-sensor_volt)/sensor_volt; // omit *RL stała gazowa Rs
  ratio = RS_gas/1.85;  // ratio = RS/R0 ze wzorku l ratio
  if (Serial2.available())
  {
  // lokalnie na esp32 do debuglarzu
  Serial.print(ratio);
  Serial.print("\t");
  Serial.print(pulse_volt);  
  Serial.print("\n");
  // wysyłka do rbpi
  Serial2.print("g");
  Serial2.print(ratio);
  Serial2.print("\n");
  Serial2.print("h");
  Serial2.print(pulse_volt);
  Serial.print("\n");
  delay(50);
  }
}