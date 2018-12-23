#include <Servo.h>

char data = '0';
int val = -1;

// servo movements signals from arduino
int left    = 0;
int right   = 0;
int angleX  = 0;
int angley  = 0;

// create servo object to control a servo
Servo myservo;

void setup() {
  
Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
myservo.attach(9);    // attaches the servo on pin 9 to the servo object

}

void loop() {

    // read from serial while data is available
    while(Serial.available()){
      data = Serial.read();        
    }

    // convert to int 
    // value sent from keyboard is = 65 + (a combination of 4 bits )
    val = data - 65 ;

    // each bit of represents the button pressed on keyboard
    left = val & 1<<0;
    right = val & 1<<1;
    
    if(left && angleX < 180 ){
      angleX++; 
      myservo.write(angleX);
    }
    
    if(right && angleX > 0 ){
        angleX--;
        myservo.write(angleX);
    }
}
