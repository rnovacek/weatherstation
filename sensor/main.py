
import sys

if sys.platform == 'esp8266':
    print('Running on ESP')
    from si7021 import Si7021
    import urequests
    from machine import RTC, deepsleep, DEEPSLEEP, DEEPSLEEP_RESET, reset_cause, ADC, Pin
    from network import WLAN, STA_IF, AP_IF
    from time import sleep_ms, sleep_us, ticks_ms, ticks_diff
    from onewire import OneWire
    from ds18x20 import DS18X20

else:
    print('Running on desktop')
    import requests as urequests
    sys.path.insert(0, "../common")
    from fake import (
        Si7021, RTC, deepsleep, DEEPSLEEP, DEEPSLEEP_RESET, reset_cause, WLAN, STA_IF, AP_IF, sleep_ms, sleep_us, ticks_ms, ticks_diff, ADC, OneWire, Pin, DS18X20
    )

from wemos import WEMOS_MAPPING
from config import TEMP_SENSORS, SERVER_URL, NODE, SSID, PASSWORD, INTERVAL


def debug(s, *args):
    print(s % args)


def read_battery_voltage():
    """Read battery voltage and return percent of charge"""

    # There is 100k resistor connecting A0 to battery and Wemos D1 mini has 100k + 220k resistors
    # The ADC has 1024 levels
    voltage = ADC(0).read() / 1024.0 * 4.2

    # voltage should be in range of 4.2V (fully charged or charging) and ~2.5V (discharge protection should kick in)
    return (voltage - 2.5) / (4.2 - 2.5) * 100


# Workaround for bug with OneWire communication
# https://github.com/micropython/micropython/issues/4116

def reset(self, required=False):
    self.pin.value(0)
    sleep_us(480)
    self.pin.value(1)
    sleep_us(70)
    status = self.pin.value()
    sleep_us(420)
    return status

OneWire.reset = reset

# End of workaround

class DS18:
    def __init__(self, pin_number):
        pin = Pin(pin_number)
        ow = OneWire(pin)
        self.ds = DS18X20(ow)
        self.devices = None
        for i in range(10):
            self.devices = self.ds.scan()
            if self.devices:
                break
            sleep_ms(100)

    def read_temp(self):
        if not self.devices:
            return None

        self.ds.convert_temp()
        sleep_ms(750)
        return self.ds.read_temp(self.devices[0])

    def read_humidity(self):
        return None


class Main:
    HEADERS = {
        'Content-Type': 'application/json',
    }

    def __init__(self, sensor, logger_url):
        self.sensors = sensors
        self.logger_url = logger_url

    def read(self):
        results = []
        for sensor in self.sensors:
            results.append({
                'name': sensor.name,
                'temperature': sensor.read_temp(),
                'humidity': sensor.read_humidity(),
            })
        return results

    def send(self, readings, battery):
        data = {
            'readings': readings,
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
        self.ap = WLAN(AP_IF)
        self.ap.active(False)

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

    sensors = []
    for name, sensor in TEMP_SENSORS.items():
        if sensor['type'] == 'si7021':
            s = Si7021(
                sda_pin=WEMOS_MAPPING[sensor['sda_pin']],
                scl_pin=WEMOS_MAPPING[sensor['scl_pin']],
            )
        elif sensor['type'] == 'ds18x20':
            s = DS18(pin_number=WEMOS_MAPPING[sensor['pin']])
        else:
            raise ValueError('Invalid sensor type: {}'.format(sensor['type']))

        s.name = name
        sensors.append(s)

    m = Main(sensors, SERVER_URL)

    m.connect(SSID, PASSWORD)

    delta = ticks_diff(ticks_ms(), start)
    debug('read starting %s', delta)

    readings = m.read()
    for reading in readings:
        debug(
            'Name: {name}, Temp: {temperature}, Humidity: {humidity}%%'.format(
                name=reading['name'], temperature=reading['temperature'], humidity=reading['humidity']
            )
        )

    delta = ticks_diff(ticks_ms(), start)
    debug('read finished %s', delta)

    battery = read_battery_voltage()
    debug('Battery: %.1f%%', battery)

    if m.wait_for_connection():
        delta = ticks_diff(ticks_ms(), start)
        debug('sending %s', delta)
        m.send(readings, battery)

    delta = ticks_diff(ticks_ms(), start)
    debug('time spent %s', delta)

    debug('Deepsleeping for %s', INTERVAL)
    m.deepsleep(INTERVAL)
