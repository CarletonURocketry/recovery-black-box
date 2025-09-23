# Version 6: Client Pico

# Based on: Tony Goodhew 5 July 2022
# Modified by: Nasu Caplan, Jordan Trach, Mahin Akond
import network
import time
import machine
from machine import Pin, ADC
from picozero import pico_led
import socket
import select
import noisemaker as m
from noisemaker import melody, melody2
#import test

ssid = "NAME"
password = "PASSWORD"

#Initialize Pins
inputPin = Pin(10, Pin.OUT,Pin.PULL_DOWN)
led2 = Pin(11, Pin.OUT)
led3 = Pin(12, Pin.OUT)
led4 = Pin(13, Pin.OUT)
pwm27 = machine.PWM(Pin(27))

led2.value(0)
led3.value(0)
led4.value(0)

charge_sent=False
interrupt_flag=False

#create a file named flight_log to store flight data
log_filename_client ="flightLog_client.csv"

m.play_melody(pwm27, melody)

#Set up WLAN object in station mode (STA - client)
wlan = network.WLAN(network.STA_IF)
#Activate WLAN
wlan.active(True)
#Configure the WLAN to IP 192.168.4.22
wlan.ifconfig(('192.168.4.22','255.255.255.0', '192.168.4.1', '192.168.4.1'))
#Set pico WLAN to not conserve power for wifi module
wlan.config(pm= 0xa11140, channel=3)
#Connect to AP module with username and password
wlan.connect(ssid, password)

#####################Function to log flight entries#####################
#Overwrites the client flight log CSV file (no data is saved - clears storage)
with open(log_filename_client, "a") as file:
    file.write("Timestamp,Event\n")
    
def callback(inputPin):
    global interrupt_flag
    interrupt_flag=True
    print("Trigger Occured: Pin 10 is Increasing")


inputPin.irq(trigger=Pin.IRQ_RISING, handler=callback)

def log_eventc(event):
    # Get current timestamp
    #timestamp = time.localtime()
    #readable_time = f"{timestamp[0]}-{timestamp[1]:02}-{timestamp[2]:02} {timestamp[3]:02}:{timestamp[4]:02}:{timestamp[5]:02}"
   
    with open(log_filename_client, "a") as log_file:
        #log_file.write(f"{readable_time},{event}\n")
        log_file.write(f"{event}\n")
   
    #print(f"{readable_time} - {event}")
    print(f"{event}")


#####################Connect to AP Pico ################################   
def connect():
    print("Connecting to:",ssid)
    
    #Check if Client Pico is connected to AP
    while wlan.isconnected() == False:
        pico_led.on()
        time.sleep(0.5)
        pico_led.off()
        time.sleep(0.5)
        pico_led.on()
        time.sleep(0.5)
        pico_led.off()
        print('Waiting for connection...')
        print(wlan.isconnected())
        time.sleep(1)
    
    # Should be connected and have an IP address
    pico_led.on()   
    print("Connected:",wlan.isconnected())
    

    wlan.status() # 3 == success
   
    print(wlan.ifconfig())
    
    #log blackbox connection event
    log_eventc("Blackbox connected")
    
    led2.value(1)
    time.sleep(1)
    led3.value(1)
    time.sleep(1)
    led4.value(1)
    time.sleep(2)
    led2.value(0)
    led3.value(0)
    led4.value(0)
    time.sleep(1)
    
################## Client socket connection with AP ######################
    
def client(charge_sent,wlan):
    #Set up IP adress connection to AP socket server
    ai = socket.getaddrinfo("192.168.4.1", 80)
    addr = ai[0][-1]
    print(addr)
    #Create a socket object for the client
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Try connecting client to server socket connection
    try:
        client.connect(addr)
    except OSError as e:
        pico_led.off()
        time.sleep(2)
        print('A connection error happened')
        
    m.play_melody(pwm27, melody2)
    
    while True:
        # Store reply and print what was received
        print('Waiting to receive')
        data = client.recv(1024)
        
        #log the received data
        #log_eventc(f"Received from Purplebox: {data}")
        #Check Data received
        if data == b"False" and not interrupt_flag:
            #Data sent from server indicate no charge sent 
            led3.value(1)
            time.sleep(0.02)
            led3.value(0)
            print('Received:', data)
      
        if data == b"True" or interrupt_flag:   
            # Data sent from server indicates charge was sent
            led2.value(1)
            led3.value(1)
            led4.value(1)
            
            inputPin.value(1) #GPIO10 ON (Send charge to e-match)
            
            #charge_sent=True
            #log when charge is sent to blackbox
            log_eventc("Charge sent to Blackbox")
            break
        
        #Indicate to server that client received data
        client.send(b'Received')
        
        #Break out of code and close connection/socket when charge is sent
        if interrupt_flag:
            client.close()
            break
        
try:
    connect()
    client(charge_sent,wlan)
    
except Exception as error:
    led2.value(1)
    led4.value(1)
    time.sleep(1)
    
    print('Error:', type(error))
    #Machine.reset() causes the USB connection to be cut, soft reset if there is a connection issue
    machine.soft_reset() 

