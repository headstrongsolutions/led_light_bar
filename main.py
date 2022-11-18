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
        self.patterns = [
            ["Rainbow Cycle", self.rainbow_cycle],
            ["Cycle", self.cycle],
            ["Chase Colour (default)", self.chase_colour],
            # ["Chase Colour (Green)", self.chase_colour((0,255,0))],
            # ["Chase Colour (Blue)", self.chase_colour((0,0,255))],
            # ["Chase Colour (White)", self.chase_colour((255,255,255))],
            ["Fill Colour (Default)", self.fill_colour],
            ["Fade (Default)", self.fade]
        ]

    def change_selected_pattern(self, new_index):
        min = 0
        max = len(self.patterns) -1
        if new_index > max:
            self.selected_pattern = min
        elif new_index < min:
            self.selected_pattern = max
        else:
            self.selected_pattern = new_index
        print(self.selected_pattern)


    def rotary_changed(self, change):
        self.run_pattern = not self.run_pattern
        if change == Rotary.ROT_CW:
            new_index = self.selected_pattern + 1
            self.change_selected_pattern(new_index)
            self.run_pattern = True
        elif change == Rotary.ROT_CCW:
            new_index = self.selected_pattern - 1
            self.change_selected_pattern(new_index)
            self.run_pattern = True
        elif change == Rotary.SW_RELEASE:
            self.run_pattern = not self.run_pattern
            if not self.run_pattern:
                self.clear()
    
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


    def cycle(self):
        if self.run_pattern:
            for i in range(4 * self.led_count):
                if self.run_pattern:
                    for j in range(self.led_count):
                        self.strip[j] = (0, 0, 0)
                    if self.run_pattern:
                        self.strip[i % self.led_count] = (255, 255, 255)
                        self.strip.write()
                        sleep(0.0000001)

    def fade(self):
        if self.run_pattern:
            for i in range(0, 4 * 256, 8):
                if self.run_pattern:
                    for j in range(self.led_count):
                        if self.run_pattern:
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
        if self.run_pattern:
            for i in range(0, self.led_count):
                if self.run_pattern:
                    self.strip.fill((0,0,0))
                    self.strip[i] = color
                    self.strip.write()
                    sleep(0.0000001)

    def rainbow_cycle(self, wait=0.00001):
        for j in range(255):
            for i in range(self.led_count):
                if self.run_pattern:
                    pixel_index = (i * 256 // self.led_count) + j
                    self.strip[i] = self.wheel(pixel_index & 255)
            self.strip.write()
            sleep(wait)

if __name__ == "__main__":
    led_strip = LedStrip(pin = 0,led_count = 96, rotary_switch_pin = 3, rotary_clk_pin = 2, rotary_dt_pin = 4)
    while True:
        led_strip.patterns[led_strip.selected_pattern][1]()
