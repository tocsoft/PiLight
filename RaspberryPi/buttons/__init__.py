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
        currentTime = time.clock()
        for x in range(0, 3):
            if current[x] != _state[x]:
                _lastChanged[x] = currentTime
            if (currentTime - _lastChanged[x]) > _debounceLimit :
                if current[x] != _state[x]:
                    _state[x] = current[x]
                    print ('button', x, 'is', _state[x] )
        

_thread = threading.Thread(target=_loop, args=())
_thread.start()