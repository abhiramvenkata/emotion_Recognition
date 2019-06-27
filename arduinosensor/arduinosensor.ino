qd#include <dht.h>
const int pingPin = 7;  //ultra sonic sensor
const int echoPin = 6; 
#define Heart 2  
dht DHT;
#define DHT11_PIN 3
boolean beat = false;  
void setup() {
  // put your setup code here, to run once:
analogReference(INTERNAL);
pinMode(Heart, INPUT);
Serial.begin(9600);
}

void loop() {
 long duration=0,h=0;
pinMode(pingPin, OUTPUT);
digitalWrite(pingPin, LOW);
delayMicroseconds(2);
digitalWrite(pingPin, HIGH);
delayMicroseconds(10);
digitalWrite(pingPin, LOW);
pinMode(echoPin, INPUT);

duration = pulseIn(echoPin, HIGH);
h=duration/58;
h=25-h;
//if(h<10)
{
  digitalWrite(13,HIGH);
  Serial.print("   the height of the saline remaining is    ");   
  Serial.print(h);
  Serial.print("cm    ");
}
if(digitalRead(Heart)>0){               
    if(!beat){                            
      beat=true;                          
      Serial.print("    present heart beat");               
    }
}
    int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.print(DHT.temperature);
  Serial.print("     Humidity = ");
  Serial.println(DHT.humidity);
delay(1000);// put your main code here, to run repeatedly:

}
