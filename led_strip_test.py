from machine import Pin
from neopixel import NeoPixel
from time import sleep
from rotary import Rotary

class LedStrip:
    def __init__(self,
                 pin: int,
                 led_count: int,
                 rotary_switch_pin: int,
                 rotary_clk_pin: int,
                 rotary_dt_pin: int):
        self.led_count = led_count
        self.strip = NeoPixel(Pin(pin, Pin.OUT), self.led_count)
        self.rotary = Rotary(dt=rotary_dt_pin, clk=rotary_clk_pin, sw=rotary_switch_pin)
        self.rotary.add_handler(self.rotary_changed)
        self.run_pattern = True
        self.selected_pattern = 0

    def rotary_changed(self, change):
        if change == Rotary.ROT_CW:
            self.selected_pattern += 1
            print(self.selected_pattern)
        elif change == Rotary.ROT_CCW:
            self.selected_pattern -= 1
            print(self.selected_pattern)
        elif change == Rotary.SW_PRESS:
            print('PRESS')
        elif change == Rotary.SW_RELEASE:
            print('RELEASE')

    def rotary_switch_pressed(self, change):
        self.run_pattern = False
        print("button pressed")
        
    def cycle(self):
        for i in range(4 * self.led_count):
            for j in range(self.led_count):
                self.strip[j] = (0, 0, 0)
            self.strip[i % self.led_count] = (255, 255, 255)
            self.strip.write()
            sleep(0.0000001)

    def bounce(self):
        for i in range(4 * self.led_count):
            for j in range(self.led_count):
                self.strip[j] = (0, 0, 128)
            if (i // self.led_count) % 2 == 0:
                self.strip[i % self.led_count] = (0, 0, 0)
            else:
                self.strip[self.led_count - 1 - (i % self.led_count)] = (0, 0, 0)
            self.strip.write()
            sleep(0.0000001)

    def fade(self):
        for i in range(0, 4 * 256, 8):
            for j in range(self.led_count):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self.strip[j] = (val, 0, 0)
            self.strip.write()

    def clear(self):
        for i in range(self.led_count):
            self.strip[i] = (0, 0, 0)
        self.strip.write()
    
    def fill_colour(self, color=(255,255,255)):
        self.strip.fill(color)
        self.strip.write()
        sleep(0.0000001)
    
    def chase_colour(self, color=(255,0,0)):
        for i in range(0, self.led_count):
            self.strip.fill((0,0,0))
            self.strip[i] = color
            self.strip.write()
            sleep(0.0000001)

    def wheel(self, pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b)

    def rainbow_cycle(self, wait=0.0000001):
        for j in range(255):
            for i in range(self.led_count):
                pixel_index = (i * 256 // self.led_count) + j
                self.strip[i] = self.wheel(pixel_index & 255)
            self.strip.write()
            sleep(wait)
            
if __name__ == "__main__":
    led_strip = LedStrip(pin = 0,led_count = 96, rotary_switch_pin = 3, rotary_clk_pin = 2, rotary_dt_pin = 4)
    while led_strip.run_pattern:
        # multiple patterns )
        print("starting cycle")
        led_strip.cycle()
        #led_strip.chase_colour()
        #led_strip.chase_colour((0,255,0))
        #led_strip.chase_colour((0,0,255))
        #led_strip.chase_colour((255,255,255))
        #led_strip.fill_colour()
        #led_strip.cycle()
        #led_strip.bounce()
        #led_strip.fade()
        #led_strip.fill_colour((0,0,0))
    print("stopped")
