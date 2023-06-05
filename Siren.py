import time
import threading
import logging

from gpiozero import OutputDevice

logger = logging.getLogger('app_logger')

class Siren():
    sirenSwitch=0
    sounding=0
    soundTimeS=0
    
    def __init__(self, outputPin):
        logger.info("Using pin " + str(outputPin) + " as siren switch")
        self.sirenSwitch = OutputDevice(outputPin)
        self.sirenSwitch.off()
    
    def _sound(self):
        logger.info("starting sound loop")
        
        self.sounding=1
        self.sirenSwitch.on()
        self.soundTimeS = 60*10
        while self.soundTimeS>0:
            time.sleep(1)
            self.soundTimeS = self.soundTimeS - 1
        self.sirenSwitch.off()
        self.sounding=0
        
        logger.info("leaving sound loop")
    
    
    def isSounding(self):
        return self.sounding
    
    def chirp(self, count=1):
        logger.info("chirp count: " + str(count))
        if self.sounding==0:
            while count > 0:
                self.sirenSwitch.on()
                time.sleep(0.05)
                self.sirenSwitch.off()
                time.sleep(0.2)
                count = count - 1
        
        
    def sound(self, soundTimeS):
        logger.info("sound")
        self.soundTimeS = soundTimeS
        if self.sounding==0:
            self.sounding=1
            threading.Thread(target=self._sound).start()
        
    def stop(self):
        logger.info("stop")
        self.soundTimeS=0
        