from LoggingConfig import LoggingConfig
LoggingConfig.configureLogging()

from SensorMonitor import SensorMonitor
from Siren import Siren
from AlarmToggleSwitch import AlarmToggleSwitch
from EmailNotification import EmailNotification

#from gpiozero import LED

from enum import Enum

import RPi.GPIO as GPIO  
import time
import logging
import os

import configparser
config = configparser.ConfigParser()
configFilePath = r'app.ini'
config.read(configFilePath)

class State(Enum):
    DISARMED = 0
    ARMING = 1
    MONITORING = 2
    TRIPPED = 3
    SOUNDING = 4


logger = logging.getLogger('app_logger')

alarmTripWarnTimeS = int(config.get('config', 'alarm_trip_warn_time_s'))
alarmSoundTimeS = int(config.get('config', 'alarm_sound_time_s'))
alarmArmDelayS = int(config.get('config', 'alarm_arm_delay_s'))

logger.info("alarmTripWarnTimeS: " + str(alarmTripWarnTimeS))
logger.info("alarmSoundTimeS: " + str(alarmSoundTimeS))
logger.info("alarmArmDelayS: " + str(alarmArmDelayS))

pulseTimeS = 2

stateElapsedTimeS = 0

emailNotification = EmailNotification()

state = State.DISARMED


#led = LED(6)
#led.on()
#led.blink(on_time=1,off_time=1)

def sendNotification(msg):
    global logger
    logger.info("sendNotification: " + msg)
    
    global emailNotification
    emailNotification.send("alarm notification!!!", msg)
    
    #os.system("sh twilio_sms.sh " + msg)
    #os.system("sh email.sh " + msg)



def alarmToggleSwitch():
    
    global state
    
    logger.info("alrmToggleSwitch, current state: " + str(state))
    
    if state == State.DISARMED:
        setState(State.ARMING)
    else:
        setState(State.DISARMED)
    

def setState(newState):
    global stateElapsedTimeS
    global sensorMonitor
    global siren
    global state
    
    logger.info("called setState with newState: " + str(newState))
    
    if state != newState:
    
        stateElapsedTimeS = 0
    
        if newState == State.DISARMED:
            sensorMonitor.stopMonitor()
            siren.stop()
            siren.chirp()
    
        if newState == State.ARMING:
            siren.chirp(2)
        
        if newState == State.MONITORING:
            sensorMonitor.startMonitor()
            siren.chirp(3)
            
        if newState == State.TRIPPED:
            siren.chirp(3)
            sendNotification("tripped!!")
        
        if newState == State.SOUNDING:
            siren.sound(alarmSoundTimeS)
    
        state = newState
        logger.info("set state to: " + str(state))

        #global led
        #if state == 0:
        #    led.blink(on_time=1,off_time=1)
        #elif state == 1:
        #    led.blink(on_time=1,off_time=1)
        #elif state == 2:
        #    led.blink(on_time=1,off_time=1)




#########################################################
# Main
#########################################################
sensorMonitor = SensorMonitor([23,24,25])

siren = Siren(26)

alarmToggleSwitch = AlarmToggleSwitch(4,alarmToggleSwitch,[])

try:    
    sendNotification("app started")
    
    while True:
        
        if state == State.DISARMED:
            pass
        
        elif state == State.ARMING:
            if (stateElapsedTimeS > alarmArmDelayS):
                setState(State.MONITORING)

        elif state == State.MONITORING: # armed - monitor sensors
            if (sensorMonitor.getTriggeredSensorPin() > 0):
                logger.info("sensor with pin " + str(sensorMonitor.getTriggeredSensorPin()) + " triggered")
                setState(State.TRIPPED)
        
        elif state == State.TRIPPED: # tripped - countdown to alarm
            if (stateElapsedTimeS > alarmTripWarnTimeS):
                setState(State.SOUNDING)
        
        elif state == State.SOUNDING: # alarm blaring
            if (siren.isSounding() == 0):
                setState(State.MONITORING)
                
                
                
        time.sleep(pulseTimeS)
        stateElapsedTimeS = stateElapsedTimeS + pulseTimeS


except BaseException as e:
    if hasattr(e,"message"):
        sendNotification("Unexpected error: " + e.message)
    else:
        sendNotification("Unexpected error")
        
    logger.exception("main exception")
    logger.error("main exception", exc_info=e)
        
finally:
    logger.info("done")
    GPIO.cleanup()  