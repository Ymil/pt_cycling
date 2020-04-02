#define perimetromm 2079

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), interruptCount, RISING);
}

const int timeThreshold = 100;
long start_time, actual_time = 0;

void interruptCount(){
  actual_time = millis();
  if(actual_time - start_time > timeThreshold){
    start_time = actual_time;
    Serial.println(actual_time);
  }else{
    //Serial.println("Descartado");  
  }
}
