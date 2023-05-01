
import time
import re

import machine
import utime
from machine import UART
from network import WLAN
#https://github.com/nakagami/micropg Open source library for Postgres Database driver
import micropg
import pycom

pycom.heartbeat(False)
#Function to parse the time tuple in the database
def parse_tuple(input_string):
    input_string = input_string.strip("()")
    elements = input_string.split(", ")

    result = []
    for element in elements:
        if element == "None":
            result.append(None)
        else:
            result.append(int(element))

    return tuple(result)

#Connect and reconnect functions for WiFi
def connect_to_wifi(wlan, ssid):
    wlan.init(mode=WLAN.STA, ssid=ssid)
    wlan.connect(ssid=ssid, timeout=10000)
    while not wlan.isconnected():
        print("Trying to connect...")
        machine.idle()
    print("WiFi connected successfully")
    print(wlan.ifconfig())

def scan_and_connect(wlan, target_ssid):
    wlan.init(mode=WLAN.STA)
    while True:
        try:
            nets = wlan.scan()
            break
        except:
            time.sleep(3)
            pass
    for net in nets:
        if net.ssid == target_ssid:
            print('Network found!')
            wlan.connect(net.ssid, timeout=15000)
            while not wlan.isconnected():
                #machine.idle()  # save power while waiting
                print("Attempting connection...")
                time.sleep(1)
            print('WLAN connection succeeded!')
            break

def check_and_reconnect(wlan, target_ssid):
    while True:
        if wlan.isconnected():
            time.sleep(1)
            print("Connected!")
        else:
            print("Disconnected")
            time.sleep(3)
            scan_and_connect(wlan, target_ssid)

#Regex to check valid format
def is_valid_format(msg):
    #pattern = r'^\d{2}\.\d{6},-\d{2}\.\d{6}$'
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$"
    match = re.match(pattern, msg)
    return re.match(pattern, msg) is not None

#Constantly checking database to see if the value is 1
def wait_for_start_value():
    start_value_found = False

    while not start_value_found:
        cur.execute("SELECT * FROM start WHERE id = 1")

        result = cur.fetchone()
        

        if result:
            start_value_found = True
            print("Start button pressed, begginning update")

            cur.execute("UPDATE start SET id = 0")
            conn.commit()
            return
        else:
            time.sleep(1)



#Performing update if the time is different than the built in time 
def update_row_if_time_different(recname, new_rec_lat, new_rec_long, new_trans_lat, new_trans_long, new_sig_angle, conn, cur):
    rtc=machine.RTC()
    rtc.ntp_sync("pool.ntp.org")

    current_time = rtc.now()

    current_time = utime.mktime(current_time)


    cur.execute("SELECT * FROM recdata2 WHERE recname = %s", (recname,))

    row = cur.fetchone()


    if row:
        last_updated_time = row[6]

        if is_valid_format(last_updated_time):

            date_parts, time_parts = last_updated_time.split(" ")
            year, month, day = [int(x) for x in date_parts.split("-")]
            hour_str, minute_str, second_parts = time_parts.split(":")
            hour, minute = int(hour_str), int(minute_str)
            second, microsecond = [int(x) for x in second_parts.split(".")]

            time_tuple = (year, month, day, hour, minute, second, microsecond, None)

            last_updated_time = utime.mktime(time_tuple)
        else:

            time_tuple = parse_tuple(last_updated_time)
            last_updated_time = utime.mktime(time_tuple)

        if last_updated_time != current_time:

            cur.execute("""
                UPDATE recdata2
                SET rec_lat = %s, rec_long = %s, trans_lat = %s, trans_long = %s, sig_angle = %s, time_last_updated = %s
                WHERE recname = %s
            """, (new_rec_lat, new_rec_long, new_trans_lat, new_trans_long, new_sig_angle, str(time_tuple), recname))

            conn.commit()
#Function to send UART to ESP32 and then wait for data back        
def update_gui(conn, cur):

    while True:
        print("running")
        # P21 = G12 = Tx connects to GPIO 18 = Rx
        # PIN 6 IS RX for DEMO
        # PIN 5 IS TX for DEMO
        uart = UART(1, baudrate=9600, pins=('P5','P6'))
        strMsg = ''
        uart.write('esp32 check \r')
        time.sleep(1)
        if uart.any() >0:
            strMsg = uart.read().decode('utf-8')

            split_values = strMsg.split(',')

            if len(split_values) == 6:
                rec_name = float(split_values[0])
                rec_lat = float(split_values[1])
                rec_long = float(split_values[2])
                trans_lat = float(split_values[3])
                trans_long = float(split_values[4])
                sig_angle = float(split_values[5])

                
                update_row_if_time_different(rec_name, rec_lat, rec_long, trans_lat, trans_long, sig_angle, conn, cur)
                break
                
            else:
                print("not correct length in message")
            
        else:
            strMsg = "No data"
            print(strMsg)

#WiFi name
target_ssid = 'Verizon-SM-G930V-CD32'
wlan = WLAN()
pycom.rgbled(0x7f0000)
scan_and_connect(wlan, target_ssid)
pycom.rgbled(0x7f7f00)

#Creating Database connection
conn = micropg.connect(host='project403.c6uydewvrqoi.us-east-2.rds.amazonaws.com', port=5432, user='postgres',password='Nyhr7fv245', database='postgres', timeout=10000, use_ssl=False)
cur = conn.cursor()

pycom.rgbled(0x007f00)
print("Ready to press start")
wait_for_start_value()
pycom.rgbled(0x0000ff)
#Updating GUI
update_gui(conn, cur)
pycom.rgbled(0xff0000)


