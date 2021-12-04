import board
import digitalio
import adafruit_rgbled
import busio
import neopixel
import time

NUM_LEDS = 50

BRIGHTNESS = 1

CLEAR = (0, 0, 0)  # clear (or second color)

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

strip = True
count = 0 
single = 49
wheelpos = 0

color = COLORS[0]
    

led_strip = neopixel.NeoPixel(board.DATA, NUM_LEDS, brightness=BRIGHTNESS, auto_write=True)

button_boot = digitalio.DigitalInOut(board.USER_SW)
button_boot.direction = digitalio.Direction.INPUT
button_boot.pull = digitalio.Pull.UP

button_a = digitalio.DigitalInOut(board.SW_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.SW_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

led = adafruit_rgbled.RGBLED(board.LED_R, board.LED_G, board.LED_B, invert_pwm = True)

led_strip.fill(CLEAR)
try:
    with open("data.hex","rb") as file:    
        num_of_pixels = int.from_bytes(file.read(1),"little")    
        for i in range(num_of_pixels):
            num= list(file.read(3))
            led_strip[i]=tuple(num)
except OSError as e:
    led_strip.fill(CLEAR)


def button_read(button):
    return not button.value

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
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
    
def paint():
    if(strip):
        led_strip.fill(color) 
    else:
        led_strip[single] = color

while True:
    if button_read(button_a):
        count += 1
        color = COLORS[count % len(COLORS)]    
        led.color = color
        paint()
        time.sleep(0.2)
        
    if button_read(button_b):
        wheelpos += 1
        color = wheel(wheelpos % 256)    
        led.color = color
        paint()
        
    if button_read(button_boot):
        strip = not strip
        if(not strip):
            led.color = (0, 0, 255)
            led_strip.fill(CLEAR)
        paint()
        time.sleep(1)
            

    
        
        
    