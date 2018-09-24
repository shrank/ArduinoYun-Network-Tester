#include <BridgeClient.h>
#include "TimerOne.h"  
#define STATUS_OFF 1
#define STATUS_ERROR 2
#define STATUS_WARNING 3
#define STATUS_OK 4

long linuxBaud = 250000;
int  init_counter=4;
int  blink_cnt=0;
char stat[5]="\0\0\0\0";

void setup() {
  //set DIO 4-13 to output
  for(int a=4;a<14;a++)
     pinMode(a, OUTPUT);
  //LED test
    for(int a=4;a<14;a+=2)
    {
    digitalWrite(a, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(500);              // wait for a second
    digitalWrite(a, LOW);    // turn the LED off by making the voltage LOW
    }
    for(int a=5;a<14;a+=2)
   {
    digitalWrite(a, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(500);              // wait for a second
    digitalWrite(a, LOW);    // turn the LED off by making the voltage LOW
  }
  //start connection to Linux
  Timer1.initialize(500000);
  Timer1.attachInterrupt(setLED);
  Bridge.begin();
}


void setLED() {
    if(strncmp(stat,"\0\0\0\0\0",5)==0)
    {
      digitalWrite(init_counter, LOW);
      init_counter+=2;
      if(init_counter>13)
        init_counter=4;
      digitalWrite(init_counter, HIGH);
      return;
    }
    blink_cnt=blink_cnt^1;
    for(int i=0;i<5;i++)
    {
      setLEDstatus(i,stat[i]);
    }
    
}

void setLEDstatus(int n,char s){
  if(s<1 ||s>4 || s==STATUS_OFF )
  {
    digitalWrite(n*2+4,LOW);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(n*2+5,LOW );   // turn the LED on (HIGH is the voltage level)
  }
  if(s==STATUS_ERROR)
  {
    digitalWrite(n*2+4,HIGH );   // turn the LED on (HIGH is the voltage level)
    digitalWrite(n*2+5,LOW );   // turn the LED on (HIGH is the voltage level)
  }
  if(s==STATUS_WARNING)
  {
    digitalWrite(n*2+4,blink_cnt^1);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(n*2+5,blink_cnt);   // turn the LED on (HIGH is the voltage level)
  }
  if(s==STATUS_OK)
  {
    digitalWrite(n*2+4,LOW);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(n*2+5,HIGH );   // turn the LED on (HIGH is the voltage level)
  }
}

void readStatus() {
  char output[10];
  int len=Bridge.get("LED",output,10);
  int a =0;
  for(int i = 0; i<len;i++)
  {
    if (output[i] == '\n') 
       a++;
    else
    {
      if(isDigit(output[i]))
      {
        stat[a]=String(output[i]).toInt();
      }
    }
  }
}



void loop() {

  readStatus();
  delay(250);
}
