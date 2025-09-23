############################################################################
# PicoPCB 2.0 Testing Configuration
#
# Testing: 1) LED (GOOD), 2) Screw Switch(GOOD), 3) E-match 4) Buzzer(GOOD) 5) Altimeter
# 
#
############################################################################
import time
from machine import Pin, PWM
from picozero import pico_led
import noisemaker as m

GPIO10 = Pin(10, Pin.OUT)
inputPin = Pin(28,Pin.IN,Pin.PULL_UP)

led2 = Pin(11, Pin.OUT)# D2
led3 = Pin(12, Pin.OUT)# D3
led4 = Pin(13, Pin.OUT)# D4

charge_sent = False
interrupt_flag=False

def callback(inputPin):
    global interrupt_flag
    interrupt_flag=True
    print("Trigger Occured: Pin 28 is Falling")

inputPin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

GPIO10.value(0)
led2.value(0)
led3.value(0)
led4.value(0)

pico_led.on()
time.sleep(2)
############################################################################
# Test 1: LED's
############################################################################
print("starting test 1: LED Party ...")
led2.value(1)
time.sleep(1)

led3.value(1)
time.sleep(1)

led4.value(1)
time.sleep(2)

led2.value(0)
led3.value(0)
led4.value(0)
pico_led.off()
time.sleep(1)
print("Completed test 1 ...")
############################################################################
# Test 2: Screw switch
# Plug-in screw switch to correct terminals in off position
# Plug-in battery to JST connector
# Toggle screw switch to on position
# Observe LED Test 1 code
############################################################################

############################################################################
# Test 3: E-match terminals
# Plug-in screw switch to correct terminals in off position
# Plug-in battery to JST connector
# Toggle screw switch to on position
# Observe LED Test 1 code
############################################################################
print("starting test 3: E-match terminals ...")
 
time.sleep(2)

led2.value(1)
led3.value(1)
led4.value(1)

GPIO10.value(1)

time.sleep(10)

led2.value(0)
led3.value(0)
led4.value(0)

GPIO10.value(0)

print("Completed test 3: E-match terminals ...")

############################################################################
# Test 4: Buzzer
############################################################################
print("starting test 4: Buzzer ...")
pwm27 = PWM(Pin(27))

pico_led.on()

m.play_melody(pwm27)


pico_led.off()
print("Completed test 4: Buzzer ...")

led2.value(1)
time.sleep(1)

led3.value(1)
time.sleep(1)

led4.value(1)
time.sleep(2)

led2.value(0)
led3.value(0)
led4.value(0)

############################################################################
# Test 5: Altimeter terminals
############################################################################
# print("starting test 4: Altimeter terminals ...")
# while (True):
#     
#     if not interrupt_flag:
#         # Requirements: Pin 28 is high AND charge has NEVER been sent
#         led3.value(1)
#         time.sleep(0.02)
#         led3.value(0)
#         
#         print('No charge sent')
#         print("Sent: False")
#              
#     if interrupt_flag:
#         # Requirements: Pin 28 is low OR charge HAS been sent
#         print("Interrupt has occured- AP detects Pin 28 is low")
#         led2.value(1)
#         led3.value(1)
#         led4.value(1)
#         charge_sent=True
#         
#         print("Completed test 4: Altimeter terminals")
#         
#         break
# 
# 
# 

