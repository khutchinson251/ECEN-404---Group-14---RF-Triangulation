//Includes
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"
// for UART
#include <HardwareSerial.h>
#include <Arduino.h>

//Defines
//Stepper Motor Driver GPIO pin asssignments
#define STEP_GPIO  GPIO_NUM_26
#define DIR_GPIO  GPIO_NUM_27
#define RESET_GPIO  GPIO_NUM_25
#define HOMEN_GPIO  GPIO_NUM_35
#define USM0_GPIO  GPIO_NUM_32
#define USM1_GPIO  GPIO_NUM_33
// GPIO Assignements for UART
#define RX1       GPIO_NUM_16 //to pycoom gpio15
#define TX1       GPIO_NUM_17 //to pycom gpio4
#define RX2       GPIO_NUM_18 //to XBEE Tx=pin2
#define TX2       GPIO_NUM_19 //to XBEE Rx=pin3 

//Set for how long the antenna should wait in a position to get the RSSI value
#define RSSI_WAIT_TIME 5000

//Set the size of sweep around pole and how many points to check within that sweep
#define SWEEP_ANGLE 90
#define SWEEP_STEP_COUNT 10

// UART1, to Pycom
HardwareSerial MySerial1(1);
// UART2, to XBEE
HardwareSerial MySerial2(2); 

// Storing certain messages for UART
String PycomReceived1; 
String PycomReceived2;
// Specifically the XBEE sends out the GPS Coordinates
// of the TRANSMITTER
String XBeeReceived; 
// This states which receiver is transmitting data
// used for Pycom->Database
String ReceiverName;

/*
  The XBEE's were determined to have not enough directional RSSI; we
  tried 3 different antennas, 1 omnidirectional and 2 directional,
  and could not accurately determine the location of the transmitter in 
  the short AND long range tests. Because of this, we have created a 
  dictionary that will take the ideal angle of the receiver 
  of the given transmitter GPS coordinates and determine this to have the 
  strongest, ideal RSSI value of 0. Then, from there, as the receiver sweeps,
  a RSSI value corresponds to the angle checked, creating a triangle-like
  area of RSSI, where 0 is the peak and the most ideal angle. 

  Please note that this was made clear to the demo TA. RSSI was 
  attempted many, many times and unable to be used with the XBEE's.
*/
//Creating a struct to make the dictionary of key and values
struct KeyValuePair {
  float key;
  int value;
}
// 360 / 0.225 + 1 for Dictionary size
const int DICT_SIZE = 1601; 

//This is the case for when the angle given is negative it to make it the corresponding positive value
float validateKey(float keyValue) {
  if (keyValue < 0) {
    keyValue += 360;
  }
  return keyValue;
}
//Had to add in this function to make it so it wraps around to have the same value at 0 as it does 360 for the purpose
//Of having a key at 356 that it would be close to 0 when checking the poles
int wrappedDistance(float peakKeyValue, float angle) {
  int directDistance = abs(peakKeyValue - angle);
  int wrappedDistance = 360 - directDistance;
  return min(directDistance, wrappedDistance);
}

//Creating the dictionary using an absolute value function where we are able to choose where the intercept was
void createRevAbsDict(float peakKeyValue, KeyValuePair* revAbsDict) {
  float step = 0.225;

  for (int i = 0; i < DICT_SIZE; i++) {
    float angle = i * step;
    angle = validateKey(angle);
    revAbsDict[i].key = angle;

    int distance = wrappedDistance(peakKeyValue, angle);
    revAbsDict[i].value = distance;
  }
}

//Getting the value for this specific key, this is used in place for the get_rssi() function to get the
//corresponding rssi for an angle
int getValueForKey(float key, KeyValuePair* revAbsDict) {
  key = validateKey(key);
  const float epsilon = 0.001;

  for (int i = 0; i < DICT_SIZE; i++) {
    if (abs(revAbsDict[i].key - key) < epsilon) {
      return revAbsDict[i].value;
    }
  }

  return -1; // Return -1 if the key is not found
}

int get_rssi() {
    long randnum;
    randnum = random(20,51);
    int random_number = (int)randnum;
    return random_number; 
}



void step(bool step_direction, int step_speed, bool USM0, bool USM1) {

    /* Step function instructions

    direction
        1 => clockwise
        0 => counter_clockwise
    
    speed
        ms per period

    size
        00  => full step
        01  => half step
        10  => quarter step
        11  => eighth step
    
    */


    //Set delay based on period
    int pulse = step_speed / 2;

    //Set direction
    gpio_set_level(DIR_GPIO, step_direction);

    //Set step size
    gpio_set_level(USM0_GPIO, USM0);
    gpio_set_level(USM1_GPIO, USM1);

    //step once

    //set step high
    gpio_set_level(STEP_GPIO, 1);
    //set pulse size (1 = 1ms)
    vTaskDelay(pulse / portTICK_PERIOD_MS);
    
    //set step low
    gpio_set_level(STEP_GPIO, 0);
    //set pulse size (1000 = 1s)
    vTaskDelay(pulse / portTICK_PERIOD_MS);

}


int check_poles(KeyValuePair* revAbsDict) {

    //initialize variables
    int new_rssi = 0;
    int total_n_strength = 0;
    int total_s_strength = 0;
    int total_e_strength = 0;
    int total_w_strength = 0;

    //check rssi at 4 poles 3 times
    for (int i = 0; i < 3; i++) 
    {
        //get rssi at north
        vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);
        //!!!get rssi value function here!!!
        new_rssi = getValueForKey(0.000, revAbsDict);
        Serial.print("Value for key ");
        Serial.print(0.000, 3);
        Serial.print(": ");
        Serial.println(new_rssi);
        //!!!get rssi value function here!!!
        total_n_strength = total_n_strength + new_rssi;

        //move to east and get rssi
        for (int i = 0; i < 50; i++) 
        {
            step(1, 40, 0, 0);
        }
        vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);
        //!!!get rssi value function here!!!
        new_rssi = getValueForKey(90.000, revAbsDict);
        Serial.print("Value for key ");
        Serial.print(90.000, 3);
        Serial.print(": ");
        Serial.println(new_rssi);
        //!!!get rssi value function here!!!
        total_e_strength = total_e_strength + new_rssi;

        //move to south and get rssi
        for (int i = 0; i < 50; i++) 
        {
            step(1, 40, 0, 0);
        }
        vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);
        //!!!get rssi value function here!!!
        new_rssi = getValueForKey(180.000, revAbsDict);
        Serial.print("Value for key ");
        Serial.print(180.000, 3);
        Serial.print(": ");
        Serial.println(new_rssi);
        //!!!get rssi value function here!!!
        total_s_strength = total_s_strength + new_rssi;

        //move to west and get rssi
        for (int i = 0; i < 50; i++) 
        {
            step(1, 40, 0, 0);
        }
        vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);
        //!!!get rssi value function here!!!
        new_rssi = getValueForKey(270.000, revAbsDict);
        Serial.print("Value for key ");
        Serial.print(270.000, 3);
        Serial.print(": ");
        Serial.println(new_rssi);
        //!!!get rssi value function here!!!
        total_w_strength = total_w_strength + new_rssi;

        //move back to north
        for (int i = 0; i < 150; i++) 
        {
            step(0, 40, 0, 0);
        }
    }

    if ((total_n_strength < total_e_strength) && (total_n_strength < total_s_strength) && (total_n_strength < total_w_strength)) {
        return 0;
    }
    else if ((total_e_strength < total_s_strength) && (total_e_strength < total_w_strength)) {
        return 1;
    }
    else if (total_s_strength < total_w_strength) {
        return 2;
    }
    else if (total_w_strength < total_s_strength) {
        return 3;
    }
    else {
        return 4;
    }

}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  // Setup UART
  // UART1, Pycom
  MySerial1.begin(9600, SERIAL_8N1, RX1, TX1);
  // UART2, XBEE
  MySerial2.begin(9600, SERIAL_8N1, RX2, TX2);
  KeyValuePair* revAbsDict = new KeyValuePair[DICT_SIZE];
  //change the 181.125 to the angle you want it to be
  createRevAbsDict(292.5, revAbsDict);
}

void loop() {
  KeyValuePair* revAbsDict = new KeyValuePair[DICT_SIZE];
  //change the 181.125 to the angle you want it to be
  createRevAbsDict(292.5, revAbsDict);

  PycomReceived1 = MySerial1.readStringUntil('\r'); 
  // System does not start until "start signal" is sent
  if (PycomReceived1 == "esp32 check "){
    Serial.println("RECEIVED");

      //Configure GPIO pin directions
      gpio_set_direction(STEP_GPIO, GPIO_MODE_OUTPUT);
      gpio_set_direction(DIR_GPIO, GPIO_MODE_OUTPUT);
      gpio_set_direction(RESET_GPIO, GPIO_MODE_OUTPUT);
      gpio_set_direction(USM0_GPIO, GPIO_MODE_OUTPUT);
      gpio_set_direction(USM1_GPIO, GPIO_MODE_OUTPUT);
      gpio_set_direction(HOMEN_GPIO, GPIO_MODE_INPUT);

      //initialize variables
      bool j;
      int pole;
      int num_full_step;
      int num_eighth_step;
      int current_rssi;
      int best_rssi;
      float current_angle; // holds the value of the angle from north the motor is facing at any given time
      float best_angle;  
      float transmitter_direction; // degrees from north that the signal is coming from
      
      //Set reset to high so it can work
      gpio_set_level(RESET_GPIO, 1);

      //number of full steps to take per point when sweeping
      num_full_step = ((SWEEP_ANGLE / (SWEEP_STEP_COUNT - 1)) / 1.8);

      //number of eigth steps to take per point when sweeping
      num_eighth_step = (((SWEEP_ANGLE / (SWEEP_STEP_COUNT - 1)) - (num_full_step * 1.8)) / 0.225);

      current_angle = 0;
      best_rssi = 10000;
      j = 0;
      while (j == 0) {

          //run the check poles function to find which pole has strongest signal
          pole = check_poles(revAbsDict);

          //scan around the pole with strongest signal or rerun check poles
          if (pole == 0) {
              //north is best, scan around it

              //move left of pole (sweep angle / 2) degrees
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }

              //SWEEP

              //get first point
              vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

              //!!!get rssi value function here!!!
              current_rssi = getValueForKey(current_angle, revAbsDict);
              Serial.print("Value for key ");
              Serial.print(current_angle, 3);
              Serial.print(": ");
              Serial.println(current_rssi);
              if (current_rssi < best_rssi ) {
                  best_rssi = current_rssi;
                  best_angle = current_angle;
              }
              //!!!get rssi value function here!!!

              for (int i = 0; i < (SWEEP_STEP_COUNT - 1); i++) { //SWEEP_STEP_COUNT - 1 = amount of points more to take 

                  //move to next point
                  for (int j = 0; j < num_full_step; j++) 
                  {
                      step(1, 40, 0, 0);
                      current_angle = current_angle + 1.8;
                  }
                  for (int j = 0; j < num_eighth_step; j++) 
                  {
                      step(1, 40, 1, 1);
                      current_angle = current_angle + 0.225;
                  }

                  //record rssi at that point
                  vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

                  //!!!get rssi value function here!!!
                  current_rssi = getValueForKey(current_angle, revAbsDict);
                  if (current_rssi < best_rssi ) {
                      best_rssi = current_rssi;
                      best_angle = current_angle;
                  }
                  //!!!get rssi value function here!!!
                  
              }
              
              //move back to north

              //walk back the sweep (same for all poles)
              for (int i = 0; i < ((num_full_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,0,0);
                  current_angle = current_angle - 1.8;
              }
              for (int i = 0; i < ((num_eighth_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,1,1);
                  current_angle = current_angle - 0.225;
              }

              //walk from left edge of sweep to north (depending on the pole) 
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }

              //set transmitter direction at angle of strongest signal
              transmitter_direction = best_angle;


              //exit while loop
              j = 1;
          }
          else if (pole == 1) {
              //east is best, scan around it

              //move to east
              for (int i = 0; i < 50; i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }


              //move left of pole (sweep angle / 2) degrees
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }

              //SWEEP

              //get first point
              vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);
              
              //!!!get rssi value function here!!!
              current_rssi = getValueForKey(current_angle, revAbsDict);
              Serial.print("Value for key ");
              Serial.print(current_angle, 3);
              Serial.print(": ");
              Serial.println(current_rssi);
              if (current_rssi < best_rssi ) {
                  best_rssi = current_rssi;
                  best_angle = current_angle;
              }
              //!!!get rssi value function here!!!

              for (int i = 0; i < (SWEEP_STEP_COUNT - 1); i++) { //SWEEP_STEP_COUNT - 1 = amount of points more to take 

                  //move to next point
                  for (int j = 0; j < num_full_step; j++) 
                  {
                      step(1, 40, 0, 0);
                      current_angle = current_angle + 1.8;
                  }
                  for (int j = 0; j < num_eighth_step; j++) 
                  {
                      step(1, 40, 1, 1);
                      current_angle = current_angle + 0.225;
                  }

                  //record rssi at that point
                  vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

                  //!!!get rssi value function here!!!
                  current_rssi = getValueForKey(current_angle, revAbsDict);
                  if (current_rssi < best_rssi ) {
                      best_rssi = current_rssi;
                      best_angle = current_angle;
                  }
                  //!!!get rssi value function here!!!
                  
              }
              
              //move back to north

              //walk back the sweep (same for all poles)
              for (int i = 0; i < ((num_full_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,0,0);
                  current_angle = current_angle - 1.8;
              }
              for (int i = 0; i < ((num_eighth_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,1,1);
                  current_angle = current_angle - 0.225;
              }

              //walk from left edge of sweep to center of pole (same for all poles)
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }

              //move to north from east
              for (int i = 0; i < 50; i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }


              //set transmitter direction at angle of strongest signal
              transmitter_direction = best_angle;

              //exit while loop
              j = 1;
          }
          else if (pole == 2) {
              //south is best, scan around it

              //move to south
              for (int i = 0; i < 100; i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }


              //move left of pole (sweep angle / 2) degrees
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }

              //SWEEP

              //get first point
              vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

              //!!!get rssi value function here!!!
              current_rssi = getValueForKey(current_angle, revAbsDict);
              Serial.print("Value for key ");
              Serial.print(current_angle, 3);
              Serial.print(": ");
              Serial.println(current_rssi);
              if (current_rssi < best_rssi ) {
                  best_rssi = current_rssi;
                  best_angle = current_angle;
              }
              //!!!get rssi value function here!!!

              for (int i = 0; i < (SWEEP_STEP_COUNT - 1); i++) { //SWEEP_STEP_COUNT - 1 = amount of points more to take 

                  //move to next point
                  for (int j = 0; j < num_full_step; j++) 
                  {
                      step(1, 40, 0, 0);
                      current_angle = current_angle + 1.8;
                  }
                  for (int j = 0; j < num_eighth_step; j++) 
                  {
                      step(1, 40, 1, 1);
                      current_angle = current_angle + 0.225;
                  }

                  //record rssi at that point
                  vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

                  //!!!get rssi value function here!!!
                  current_rssi = getValueForKey(current_angle, revAbsDict);
                  if (current_rssi < best_rssi ) {
                      best_rssi = current_rssi;
                      best_angle = current_angle;
                  }
                  //!!!get rssi value function here!!!
                  
              }
              
              //move back to north

              //walk back the sweep (same for all poles)
              for (int i = 0; i < ((num_full_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,0,0);
                  current_angle = current_angle - 1.8;
              }
              for (int i = 0; i < ((num_eighth_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,1,1);
                  current_angle = current_angle - 0.225;
              }

              //walk from left edge of sweep to center of pole (same for all poles)
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }

              //move to north from south
              for (int i = 0; i < 100; i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }

              //set transmitter direction at angle of strongest signal
              transmitter_direction = best_angle;

              //exit while loop
              j = 1;
          }
          else if (pole == 3) {
              //west is best, scan around it

              //move to west
              for (int i = 0; i < 150; i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }


              //move left of pole (sweep angle / 2) degrees
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }

              //SWEEP

              //get first point
              vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

              //!!!get rssi value function here!!!
              current_rssi = getValueForKey(current_angle, revAbsDict);
              Serial.print("Value for key ");
              Serial.print(current_angle, 3);
              Serial.print(": ");
              Serial.println(current_rssi);
              if (current_rssi < best_rssi ) {
              best_rssi = current_rssi;
              best_angle = current_angle;
              }
              //!!!get rssi value function here!!!

              for (int i = 0; i < (SWEEP_STEP_COUNT - 1); i++) { //SWEEP_STEP_COUNT - 1 = amount of points more to take 

                  //move to next point
                  for (int j = 0; j < num_full_step; j++) 
                  {
                      step(1, 40, 0, 0);
                      current_angle = current_angle + 1.8;
                  }
                  for (int j = 0; j < num_eighth_step; j++) 
                  {
                      step(1, 40, 1, 1);
                      current_angle = current_angle + 0.225;
                  }

                  //record rssi at that point
                  vTaskDelay(RSSI_WAIT_TIME / portTICK_PERIOD_MS);

                  //!!!get rssi value function here!!!
                  current_rssi = get_rssi();
                  if (current_rssi < best_rssi ) {
                      best_rssi = current_rssi;
                      best_angle = current_angle;
                  }
                  //!!!get rssi value function here!!!
                  
              }
              
              // move back to north

              //walk back the sweep (same for all poles)
              for (int i = 0; i < ((num_full_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,0,0);
                  current_angle = current_angle - 1.8;
              }
              for (int i = 0; i < ((num_eighth_step)*(SWEEP_STEP_COUNT - 1)); i++) 
              {
                  step(0,40,1,1);
                  current_angle = current_angle - 0.225;
              }

              //walk from left edge of sweep to center of pole (same for all poles)
              for (int i = 0; i < (SWEEP_ANGLE / 3.6); i++) 
              {
                  step(1, 40, 0, 0);
                  current_angle = current_angle + 1.8;
              }

              //move to north from west
              for (int i = 0; i < 150; i++) 
              {
                  step(0, 40, 0, 0);
                  current_angle = current_angle - 1.8;
              }

              //set transmitter direction at angle of strongest signal
              transmitter_direction = best_angle;

              //exit while loop
              j = 1;
          }
          else {
              //re run check poles
              j = 0;
          }
      // XBEE "Coordinates" Read-in
      while(MySerial2.available() > 0){
        // Read in until \r, set up in transmitter code as "GPS Coordinates"
        XBeeReceived = MySerial2.readStringUntil('\r');
        if (XBeeReceived == "30.623230, -96.333884"){
          break;
        }
      }
      
      }

    /*
      This code was reused for upload on ESP32's, where we would uncomment
      the given GPS location for the receiver, the ideal angle, and the
      name of the receiver.
    */

    //String rec1 = "30.624173, -96.333953";
    //String rec1ang = "176.4";
    String rec2 = "30.622982, -96.333116";
    //rec2ang = 292.5
    //String rec3 = "30.622881, -96.334565";
    //String rec3ang = "59";

    Serial.println("RECEIVED");
    if(transmitter_direction < 0) {
      transmitter_direction += 360;
    }
    ReceiverName = "2";
    //int transmitter_direction = 45;
    String sig_angle;
    sig_angle = String(transmitter_direction);
    /* 
    Pycom wanted to be sent one long string, 
    separated by commas. Arduino does not allow for
    more than one value sent at a time without 
    stringing them together with '+'
    */
    String send_string;
    String comma;
    comma = ",";
    send_string = ReceiverName + comma + rec2 + comma +  XBeeReceived + comma + sig_angle;
    Serial.println("Rssi");
    //MySerial1.print(best_rssi);
    Serial.println(get_rssi()); 
    Serial.println("receiver number");   
    Serial.println(send_string);    
    MySerial1.print(send_string); 
    //delay(1000);
    delete[] revAbsDict;
    return;
    
  }
  delete[] revAbsDict;
}
