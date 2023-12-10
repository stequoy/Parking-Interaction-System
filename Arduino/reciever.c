#define led 4
#define prmp 8
#define prm 7
#define prd 2
#define ledPin 13

void setup() {
  pinMode(prmp, OUTPUT);
  digitalWrite(prmp, HIGH);
  pinMode(ledPin, OUTPUT); 
  pinMode(prd, OUTPUT); 
}

void loop() {
  Serial.begin(9600);
  sendCommand();
  delay(5000);
}

// посылает команду в эфир 
void sendCommand() {
  Serial.println("Command:");
  digitalWrite(ledPin, HIGH); 
  int data = digitalRead(prm);
Serial.println(data);
delay(10);
data = digitalRead(prm);
Serial.println(data);
delay(10);
data = digitalRead(prm); 
Serial.println(data);
delay(10);
data = digitalRead(prm); 
Serial.println(data);
delay(10);
data = digitalRead(prm); 
Serial.println(data);
delay(10);
data = digitalRead(prm); 
Serial.println(data);
  delay(10);
  Serial.println("End test:");
  data = digitalRead(prm); 
  Serial.println(data);
}
