# FortiThing 
## MicroPython version

This directory contains several examples with code snippets that will show how to use the different feature of FortiThing board

- Reading values such as temperature, pressure, humidity, etc.
- Setting values for leds, RGBs, etc
- Publishing the information in a MQTT server
- Subscribing to changes in MQTT server



##Examples (Ubuntu)

Use adafruit-ampy to list, add or remove files to the board.

##### List files in the board:

``` sudo ampy -p /dev/ttyUSB0 ls ```

##### Upload script to run right after board boots up:

``` sudo ampy -p /dev/ttyUSB0 put full_features_example.py /main.py```

##### Remove main.py (do it right after resetting the board)

``` sudo ampy -p /dev/ttyUSB0 rm /main.py```

##### Run/Test script in board:

``` sudo ampy -p /dev/ttyUSB0 run full_features_example.py ```

##### Check output in a separated window

``` sudo screen /dev/ttyUSB0 115200 ```

(Kill screen with Ctrl+A, Shift+K and 'y')


Enjoy!

