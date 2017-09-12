
import sys

if sys.platform == 'esp8266':
    print('Running on ESP')
    from si7021 import Si7021
    import urequests
    from machine import RTC, deepsleep, DEEPSLEEP, DEEPSLEEP_RESET, reset_cause, ADC
    from network import WLAN, STA_IF
    from time import sleep_ms, ticks_ms, ticks_diff

else:
    print('Running on desktop')
    import requests as urequests
    sys.path.insert(0, "../common")
    from fake import (
        Si7021, RTC, deepsleep, DEEPSLEEP, DEEPSLEEP_RESET, reset_cause, WLAN, STA_IF, sleep_ms, ticks_ms, ticks_diff, ADC
    )

from wemos import WEMOS_MAPPING
from config import TEMP_SDA_PIN, TEMP_SCL_PIN, SERVER_URL, NODE, SSID, PASSWORD, INTERVAL


def debug(s, *args):
    print(s % args)


def read_battery_voltage():
    """Read battery voltage and return percent of charge"""

    # There is 100k resistor connecting A0 to battery and Wemos D1 mini has 100k + 220k resistors
    # The ADC has 1023 levels
    voltage = ADC(0).read() / 1023.0 * 4.2

    # voltage should be in range of 4.2V (fully charged or charging) and ~2.5V (discharge protection should kick in)
    return (voltage - 2.5) / (4.2 - 2.5) * 100


class Main:
    HEADERS = {
        'Content-Type': 'application/json',
    }

    def __init__(self, sensor, logger_url):
        self.sensor = sensor
        self.logger_url = logger_url

    def read(self):
        return self.sensor.read_temp(), self.sensor.read_humidity()

    def send(self, temp, humidity, battery):
        data = {
            'temperature': temp,
            'humidity': humidity,
            'battery': battery,
            'sequence': 0,
            'node': NODE,
        }
        url = '{}/node/{}/temperature/add'.format(self.logger_url, NODE)
        debug('POST %s', url)
        try:
            response = urequests.post(url, json=data, headers={'Content-Type': 'application/json'})
        except OSError as e:
            debug('Failed %s', e)
            return

        if response.status_code != 200:
            debug('Failed %s', response.status_code)
        else:
            debug('Success')

    def deepsleep(self, seconds):
        rtc = RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, seconds * 1000)

        deepsleep()

    def connect(self, ssid, password):
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)

    def wait_for_connection(self):
        for _ in range(100):
            if self.wlan.isconnected():
                debug('Wifi connected: %s', self.wlan.ifconfig())
                return True
            sleep_ms(50)
        debug('Wifi timeout')
        return False


if __name__ == '__main__':
    if reset_cause() == DEEPSLEEP_RESET:
        debug('woke from a deep sleep')

    start = ticks_ms()
    debug('start %s', start)

    sensor = Si7021(
        sda_pin=WEMOS_MAPPING[TEMP_SDA_PIN],
        scl_pin=WEMOS_MAPPING[TEMP_SCL_PIN],
    )
    m = Main(sensor, SERVER_URL)

    m.connect(SSID, PASSWORD)

    delta = ticks_diff(ticks_ms(), start)
    debug('read starting %s', delta)

    temp, humidity = m.read()
    debug('Temp: %s, Humidity: %s%%', temp, humidity)

    delta = ticks_diff(ticks_ms(), start)
    debug('read finished %s', delta)

    battery = read_battery_voltage()
    debug('Battery: %.1f%%', battery)

    if m.wait_for_connection():
        delta = ticks_diff(ticks_ms(), start)
        debug('sending %s', delta)
        m.send(temp, humidity, battery)

    delta = ticks_diff(ticks_ms(), start)
    debug('time spent %s', delta)

    debug('Deepsleeping for %s', INTERVAL)
    m.deepsleep(INTERVAL)
