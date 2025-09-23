# Version 6: Transmitting Pico

# Modification: Removed log events from AP and client constant check communications
# Based on: Tony Goodhew 5 July 2022
# Modified by: Nasu Caplan, Jordan Trach, Mahin Akond
import network
import socket
import time
from machine import Pin, ADC, PWM
from picozero import pico_led
from machine import Pin
import noisemaker as m
import random
import select
# import test

ssid = "NAME"
password = "PASSWORD"

#Initialize Pins and boolean
inputPin = Pin(28,Pin.IN,Pin.PULL_UP)

led2 = Pin(11, Pin.OUT)
led3 = Pin(12, Pin.OUT)
led4 = Pin(13, Pin.OUT)
pwm27 = PWM(Pin(27))

interrupt_flag=False

m.play_melody(pwm27)

#create file to log data
log_filename_server = "flightLog_server.csv"

# Create/Append to flightlog file of server 
with open(log_filename_server,"a") as file:
    file.write("Timestamp,Event\n")

######################Function to log events#################
def log_events(event):
    # Get current timestamp
    timestamp = time.localtime()
    readable_time = f"{timestamp[0]}-{timestamp[1]:02}-{timestamp[2]:02} {timestamp[3]:02}:{timestamp[4]:02}:{timestamp[5]:02}"

# Open file and append data in CSV format
    with open(log_filename_server, "a") as log_file:
        log_file.write(f"{readable_time},{event}\n")
        #log_file.write(f"{event}\n")
    
    print(f"{readable_time} - {event}")
    print(f"{event}")


def callback(inputPin):
    global interrupt_flag
    interrupt_flag=True
    print("Trigger Occured: Pin 28 is Falling")


inputPin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

led2.value(0)
led3.value(0)
led4.value(0)
pico_led.off()

time.sleep(1)

print("Connecting to:",ssid)

#Create WLAN object that is in Access Point mode
wlan = network.WLAN(network.AP_IF)
print("WLAN Active:",wlan.active())

#Configure the SSID and Passsword before activating
wlan.config(essid=ssid,password=password)

#Activate the renamed WLAN
wlan.active(True)

#Check if AP mode has activated
while wlan.active() == False:
    pico_led.on()
    time.sleep(0.02)
    pico_led.off()
    time.sleep(0.02)
    pico_led.on()
    time.sleep(0.02)
    pico_led.off()
    print('Waiting for AP mode connection...')
    time.sleep(0.02)
    
print("WLAN status:", wlan.status()) # 3 == success
print('AP mode is Activated')
log_events("A")

# Handle connection error
if wlan.status() != 3:
    print("oh no")
    log_events(f"B")
    pico_led.off()
    raise RuntimeError(wlan.status())
else:
    pico_led.on()
    print('connected')
    ip=wlan.ifconfig()[0]
    log_events(f"C")
    print( 'ip = ' + ip )

############# Open a socket #########################

addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1] #Set IP adress for sending and receiving data connection


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create socket object

server.bind(addr)# Bind the server socket to an adress
server.listen(5) #Listening for up to five device connections

# Sockets from which we expect to read
inputs = [server]
# Sockets to which we expect to write
outputs = []

print('listening on', addr)
log_events("D")
print(server)

led2.value(1)
time.sleep(1)
led3.value(1)
time.sleep(1)
led4.value(1)
time.sleep(2)
led2.value(0)
led3.value(0)
led4.value(0)

#############Listen for connections######################

def connect():
    while True:
        print('Waiting')
        #Waits for at least one of the sockets to be ready to be monitered
        readable, writable,exceptional = select.select(inputs,outputs,inputs)
       
        
        #Handle Inputs 
        for s in readable:
            print('This is readable:', readable)
            
           # For server socket (AP)
            if s is server:
                #Server socket ready to read accept an incoming connection
                print('hello')
                cl, addr = s.accept()
                print('hello')
                cl.setblocking(0)
                inputs.append(cl)
                outputs.append(cl)
                log_events(f"E")
            else:
                #For client sockets that alrealdy connected and have sent data
                data = s.recv(1024)
                if data:
                    # A readable client socket has data
                    print(data)
                    #log_events(f"Received from client: {data}")
                    # Add socket to output list for a response
                    if s not in outputs:
                        outputs.append(s)
                
        #Handle outputs
        for s in writable:
            # if the socket is in outputs 
            if s in outputs:
                print ('This is writable:', writable)
                print('client connected from', addr)
                print("Pin 28 value",inputPin.value())
            
                if not interrupt_flag:
                    # Requirements: Pin 28 is high AND charge has NEVER been sent
                    led3.value(1)
                    time.sleep(0.02)
                    led3.value(0)
                    s.send(b'False')
                    print('No charge sent')
                    print("Sent: False")
             
                if interrupt_flag:
                    # Requirements: Pin 28 is low OR charge HAS been sent
                    print("Interrupt has occured- AP detects Pin 28 is low")
                    led2.value(1)
                    led3.value(1)
                    led4.value(1)
                    charge_sent=True
                     
                    repeat_attempts = 5 
                    for attempt in range(repeat_attempts):
                        s.send(b'True')
                        print(f"Sent: True (Attempt {attempt + 1}/{repeat_attempts})")
                        log_events(f"F")
                        time.sleep(0.1)  

                    print("Completed repeated charge attempts")
                    log_events("G")
                    #break
                #Removes socket from the ouput list - to be re-added once client responds 
                outputs.remove(s)
                
        #Handle exceptional conditions
        for s in exceptional:
            print('An exception has occurred')
            log_events("H")
            # Stop listening for input on the connection
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            
#Calls the connect function   
connect() 


