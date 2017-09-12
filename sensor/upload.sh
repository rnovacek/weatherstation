#!/bin/bash

PORT=/dev/ttyUSB0

ampy -p $PORT put main.py
ampy -p $PORT put config.py
ampy -p $PORT put si7021.py
