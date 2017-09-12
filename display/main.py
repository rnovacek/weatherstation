
import sys

if sys.platform == 'esp8266':
    print('Running on ESP')

    import dejavu
    from ssd1306 import SSD1306_I2C
    from machine import I2C, Pin
    import urequests
    from network import WLAN, STA_IF
    from time import sleep_ms

    from writer import Writer
else:
    print('Running on desktop')
    import requests as urequests
    sys.path.insert(0, "../common")
    from fake import SSD1306_I2C, I2C, Pin, Writer, dejavu, WLAN, STA_IF, sleep_ms

from wemos import WEMOS_MAPPING
from config import (
    OLED1_SDA_PIN, OLED1_SCL_PIN, OLED2_SDA_PIN, OLED2_SCL_PIN,
    TEMP_SDA_PIN, TEMP_SCL_PIN, BUTTON_PIN,
    SSID, PASSWORD, INTERVAL, SERVER_URL, NODE
)


class Main:
    DISPLAY_WIDTH = 128
    DISPLAY_HEIGHT = 32

    def __init__(self):
        i2c_1 = I2C(
            scl=Pin(WEMOS_MAPPING[OLED1_SCL_PIN]),
            sda=Pin(WEMOS_MAPPING[OLED1_SDA_PIN]))
        self.oled1 = SSD1306_I2C(self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT, i2c_1)

        i2c_2 = I2C(
            scl=Pin(WEMOS_MAPPING[OLED2_SCL_PIN]),
            sda=Pin(WEMOS_MAPPING[OLED2_SDA_PIN]))
        self.oled2 = SSD1306_I2C(self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT, i2c_2)

        self.writer1 = Writer(self.oled1, dejavu)
        self.writer2 = Writer(self.oled2, dejavu)
        
        self.wlan = WLAN(STA_IF)

    def show_data(self, temperature, humidity):
        self.show_text(
            '{:.1f} C'.format(temperature),
            '{:.1f} %'.format(humidity),
        )

    def show_text(self, text1, text2):
        self.oled1.fill(0)
        self.writer1.set_textpos(0, 0)
        self.writer1.printstring(text1)

        self.oled2.fill(0)
        self.writer2.set_textpos(0, 0)
        self.writer2.printstring(text2)

        self.oled1.show()
        self.oled2.show()

    def show_error(self, text):
        self.writer1.set_textpos(0, 0)
        self.writer1.printstring('ERROR')
        
        self.writer2.set_textpos(0, 0)
        self.writer2.printstring(text)

        self.oled1.show()
        self.oled2.show()

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(SSID, PASSWORD)
        
    def is_connected(self):
        return self.wlan.isconnected()
        
    def wait_for_connection(self):
        for _ in range(100):
            if self.wlan.isconnected():
                print('Wifi connected: %s', self.wlan.ifconfig())
                return True
            sleep_ms(50)
        print('Wifi timeout')
        return False

    def read_data(self, node):
        response = urequests.get('{}/node/{}/current'.format(SERVER_URL, node))
        if 200 <= response.status_code < 300:
            data = response.json()
            return data['temperature'], data['humidity']
        else:
            self.show_error(str(response.status_code))

    def deepsleep(self, seconds):
        rtc = RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, seconds * 1000)

        deepsleep()


if __name__ == '__main__':
    button = Pin(WEMOS_MAPPING[BUTTON_PIN], Pin.IN, Pin.PULL_UP)

    main = Main()
    main.connect()

    current_node = 1
    
    while True:
        if not main.is_connected():
            main.connect()
            if not main.wait_for_connection():
                main.show_error('WIFI')
                continue

        try:
            print('reading data')
            data = main.read_data(current_node)
            if data:
                temp, humidity = data
                print('data received: temp', temp, 'humidity', humidity)
                main.show_data(temp, humidity)
        except OSError as e:
            main.show_error(str(e))

        print('Going to sleep for', INTERVAL, 'seconds')
        slept_ms = 0
        while slept_ms < INTERVAL * 1000:
            if button.value() == 0:
                sleep_ms(10)
                slept_ms += 10
                if button.value() == 0:
                    print('button pressed')
                    if current_node == 1:
                        current_node = 2
                    else:
                        current_node = 1
                    main.show_text('SENSOR', str(current_node))
                    break
            sleep_ms(10)
            slept_ms += 10
