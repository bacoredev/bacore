"""DEVONthink3 interface."""

from pydt3 import DEVONthink3

try:
    dt = DEVONthink3()
except RuntimeError:
    raise RuntimeError("DEVONthink3 is not installed.")
