long randNumber;

void setup() {
  Serial.begin(9600);
}

void loop(){
  randNumber = random(100, 1000);
  delay(randNumber);
  Serial.println(millis());
}
