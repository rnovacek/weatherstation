# DIY Home Weather Station

This project aims to create simple home weather station to provide basic information about weather (temperature and humidity so far) inside and outside.

This project has several parts:

* Solar powered temperature and humidity wireless sensor with battery backup
* Web Application to store temperature information that has both API and web page to provide gathered information
* Indoor sensor unit with display

Both sensor units are powered by ESP8266 chip (I'm using Wemos D1 mini) and programmed in MicroPython.

## Outdoor sensor unit

* Wemos D1 mini (ESP8266)
* Solar panel 5V 1.25W
* 18650 battery
* TP4056 based battery charger
* 5V voltage booster
* Si7021 Humidity and Temperature sensor

## Indoor sensor and display unit

* Wemos D1 mini (ESP8266)
* 2x 0.91 inch 128x32 OLED display (SSD1306)
* Si7021 Humidity and Temperature sensor
* button

# Server and webapp

* Server written in Python (Flask)
* React based WebApp
