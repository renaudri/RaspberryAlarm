import time
import threading
import logging

from gpiozero import Button

logger = logging.getLogger('app_logger')

class AlarmToggleSwitch():
    
    armToggleButton = 0
    armToggleMethod = 0
    combination = [] # required button combination to arm / disarm (list of short / long presses)
    
    def __init__(self, buttonPin, armToggleMethod, combination):
        
        logger.info("using pin " + str(buttonPin) + " for alarm toggle")
        
        self.armToggleButton = Button(buttonPin)
        self.armToggleButton.when_released = self._buttonReleaseEvent
        self.armToggleButton.when_pressed = self._buttonPressedEvent
        
        self.armToggleMethod = armToggleMethod
        
        self.combination = combination
        
        
    def _buttonPressedEvent(self):
        logger.info("_buttonPressedEvent")
        
    def _buttonReleaseEvent(self):
        logger.info("_buttonReleaseEvent")
        self.armToggleMethod()