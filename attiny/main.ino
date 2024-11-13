void setup()
{
  const int waitFor = 7200000; // 2h in ms
  const int rpiPin = 0;

  pinMode(rpiPin, OUTPUT);
  digitalWrite(rpiPin, HIGH);
}

void loop()
{
  delay(waitFor);
  digitalWrite(rpiPin, LOW);

  delay(10);
  digitalWrite(rpiPin, HIGH);
}
