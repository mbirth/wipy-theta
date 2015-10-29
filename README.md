RICOH THETA m15 Remote for the WiPy
===================================

Use a [WiPy](http://wipy.io/) to connect to a [RICOH THETA](https://theta360.com/) camera
and trigger the shutter remotely.

As I'm using the Expansion Board, the shutter button is connected to GP17 and pulling the pin low.
A LED is connected to GP16.


Preparation
-----------

Copy the `config.example.py` to `config.py` and adjust the constants to your home wifi network.

If you want to try the script from a desktop computer, install all needed dependencies with:

    micropython -m upip install -r requirements.txt


Connecting to the THETA
-----------------------

When you switch on WiFi on your THETA, it creates a network called `THETA` followed by its serial
number, e.g. `THETAXN20123456`. The numeric part of the serial number is the password.
(Only if you didn't change it in the THETA app.)
