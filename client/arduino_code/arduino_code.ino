#include <Time.h>
#include <TimeLib.h>


String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

#define perimetromm 2079

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
 /* String datetime = Serial.readString();
  int h = getValue(datetime, " ", 0).toInt();
  int m = getValue(datetime, " ", 1).toInt();
  int s = getValue(datetime, " ", 2).toInt();
  int D = getValue(datetime, " ", 3).toInt();
  int M = getValue(datetime, " ", 4).toInt();
  int Y = getValue(datetime, " ", 5).toInt();
  setTime(h,m,s,D,M,Y);
  Serial.println(datetime);*/
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), interruptCount, RISING);
}

const int timeThreshold = 100;
long start_time, actual_time = 0;

void interruptCount(){
  actual_time = millis();
  if(actual_time - start_time > timeThreshold){
    start_time = actual_time;
/*    time_t t = now(); 
    Serial.print(hour(t));
    Serial.print(":");
    Serial.print(minute(t));
    Serial.print(":");
    Serial.print(second(t));
    Serial.print(".");*/
    Serial.println(actual_time);
  }else{
    //Serial.println("Descartado");  
  }
}
void loop() {
  // put your main code here, to run repeatedly:

}
