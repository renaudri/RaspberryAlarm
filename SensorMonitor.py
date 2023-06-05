import time
import threading
import logging

from gpiozero import Button

logger = logging.getLogger('app_logger')

class SensorMonitor():
    
    contacts = []
    monitoring = 0
    triggeredPinNumber = 0
    
    def __init__(self, contactPins):
        
        for contactPin in contactPins:
          self.contacts.append(Button(contactPin))
          logger.info("added sensor with pin " + str(contactPin))
    
    def _monitorSensors(self):
        logger.info("starting monitor Sensor loop")
        
        contactPositions = []
        for contact in self.contacts:
            contactPositions.append(contact.is_pressed)
            
        while self.monitoring == 1:
            i = 0
            while i < len(self.contacts):
                if (self.contacts[i].is_pressed != contactPositions[i]):
                    contactPositions[i] = self.contacts[i].is_pressed
                    logger.info("triggered!!")
                    self.triggeredPinNumber = self.contacts[i].pin.number
                i = i + 1
                
            time.sleep(1)
        
        logger.info("exiting monitor sensor")
        
    
    def startMonitor(self):
        if self.monitoring == 0:
            logger.info("monitoring")
            self.monitoring = 1
            self.triggeredPinNumber = 0
            threading.Thread(target=self._monitorSensors).start()
        
    def stopMonitor(self):
        if self.monitoring == 1:
            logger.info("stop")
            self.monitoring = 0
            self.triggeredPinNumber = 0
    
    def getTriggeredSensorPin(self):
        return self.triggeredPinNumber;
        