import machine
import utime as time
from machine import Pin
import micropython

class Rotary:
    
    ROT_CW = 1
    ROT_CCW = 2
    SW_PRESS = 4
    SW_RELEASE = 8
    
    def __init__(self,dt,clk,sw):
        self.dt_pin = Pin(dt, Pin.IN, Pin.PULL_DOWN)
        self.clk_pin = Pin(clk, Pin.IN, Pin.PULL_DOWN)
        self.sw_pin = Pin(sw, Pin.IN, Pin.PULL_DOWN)
        self.last_status = (self.dt_pin.value() << 1) | self.clk_pin.value()  # type: ignore
        self.dt_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.clk_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.sw_pin.irq(handler=self.switch_detect, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.handlers = []
        self.last_button_status = self.sw_pin.value()
        
    def rotary_change(self, pin):
        new_status = (self.dt_pin.value() << 1) | self.clk_pin.value()  # type: ignore
        if new_status == self.last_status:
            return
        transition = (self.last_status << 2) | new_status  # type: ignore
        try:
            if transition == 0b1110:
                micropython.schedule(self.call_handlers, Rotary.ROT_CW)
            elif transition == 0b1101:
                micropython.schedule(self.call_handlers, Rotary.ROT_CCW)
        except RuntimeError:
            # ugly ,but valid: https://www.coderdojotc.org/micropython/sensors/10-rotary-encoder/
            pass
        self.last_status = new_status
        
    def switch_detect(self,pin):
        if self.last_button_status == self.sw_pin.value():
            return
        self.last_button_status = self.sw_pin.value()
        try:
            if self.sw_pin.value() and self.sw_pin.value() == 1:
                micropython.schedule(self.call_handlers, Rotary.SW_RELEASE)
            else:
                micropython.schedule(self.call_handlers, Rotary.SW_PRESS)
        except RuntimeError:
            # ugly ,but valid: https://www.coderdojotc.org/micropython/sensors/10-rotary-encoder/
            pass
            
    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def call_handlers(self, type):
        for handler in self.handlers:
            handler(type)
