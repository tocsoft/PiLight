import math
import automationhat
import time
import threading

_state = [
    0,
    0,
    0
]
_startTime = time.clock()
# so we delay before seeing a 
_lastChanged = [
    _startTime ,
    _startTime ,
    _startTime 
]
_downTime = [
    _startTime ,
    _startTime ,
    _startTime 
]
_upTime = [
    0,
    0,
    0
]

_eventWaiting= [
    0,
    0,
    0
]
_debounceLimit = 10
_longPressLimit = 1000

def _loop():
    global _startTime
    global _lastChanged
    global _debounceLimit
    global _downTime
    global _upTime
    global _eventWaiting
    global _longPressLimit

    while True:
        # monitoring loop cehck status of each input and raise correct events for each
        current = [
            automationhat.input.one.read(),
            automationhat.input.two.read(),
            automationhat.input.three.read()
        ]
        print (current)
        
_thread = threading.Thread(target=_loop, args=())
_thread.start()