void setup(){
Serial.begin(9600) ;
}
void loop()
{
for (char i = 0; i < 50; i++)
{
    Serial.println("Deneme");
    delay(1000);
    if (i=49)
    {   
        i=0;
        Serial.println("sıfırlandı");
    }
 }
}
