
import time
import random


class Si7021:
    def __init__(self, scl_pin, sda_pin):
        pass

    def read_temp(self):
        return 25 + random.randint(-5, 5)

    def read_humidity(self):
        return 50 + random.randint(-25, 25)


def sleep_ms(ms):
    time.sleep(ms / 1000.0)


def sleep_us(us):
    time.sleep(ms / 1000000.0)


def ticks_ms():
    return time.time() * 1000


def ticks_diff(a, b):
    return a - b


# machine.py

DEEPSLEEP = 'deepsleep'
DEEPSLEEP_RESET = 'deepsleep'


class RTC:
    ALARM0 = 0
    seconds = None
    cause = None

    def irq(self, trigger, wake):
        pass

    def alarm(self, trigger, seconds):
        RTC.seconds = seconds


def deepsleep():
    RTC.cause = DEEPSLEEP_RESET
    if RTC.seconds is None:
        raise RuntimeError('RTC not configured')
    sleep_ms(RTC.seconds)


def reset_cause():
    return RTC.cause


STA_IF = 0
AP_IF = 1


class WLAN:
    is_active = False

    def __init__(self, type):
        pass

    def active(self, active):
        is_active = active

    def connect(self, ssid, password):
        self.start = time.time()

    def ifconfig(self):
        return 'IFCONFIG'

    def isconnected(self):
        return time.time() - self.start > 2


class ADC:
    def __init__(self, index):
        pass

    def read(self):
        # random float between 2.5 and 4.2
        voltage = 2.5 + random.random() * (4.2 - 2.5)
        # ADC return 0 - 1023
        return voltage / 4.2 * 1023


class I2C:
    def __init__(self, scl, sda):
        self.scl = scl
        self.sda = sda

    def __str__(self):
        return 'I2C({}, {})'.format(self.scl, self.sda)


class SSD1306_I2C:
    def __init__(self, width, height, i2c):
        self.i2c = i2c

    def poweron(self):
        print('Powering on display', self.i2c)

    def show(self):
        print(self.i2c, 'show')

    def fill(self, value):
        print(self.i2c, 'filling with', value)


class Pin:
    IN = 1
    OUT = 2
    PULL_UP = True

    def __init__(self, pin, direction=OUT, pull_up=None):
        self.pin = pin
        self.direction = direction
        self.pull_up = pull_up

    def __str__(self):
        return '<{}>'.format(self.pin)

    def value(self):
        return 1


class Writer:
    def __init__(self, display, font):
        pass

    def set_textpos(self, x, y):
        self.textpos_x = x
        self.textpos_y = y

    def printstring(self, s):
        print('PRINTING at ({}, {}): {}'.format(self.textpos_x, self.textpos_y, s))


dejavu = 'dejavu'

class OneWire:
    def __init__(self, pin):
        self.pin = pin

    def reset(self):
        pass


class DS18X20:
    DEVICE = b'1234'
    def __init__(self, ow):
        pass

    def scan(self):
        return [self.DEVICE]

    def convert_temp(self):
        pass

    def read_temp(self, device):
        assert device == self.DEVICE
        return 25 + random.randint(-5, 5)
