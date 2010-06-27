# dlmain.py
from ctypes import *
h = cdll.LoadLibrary("libopenjtalk.so.1.0.1")
e = h.libopen_jtalk_main
print e()



