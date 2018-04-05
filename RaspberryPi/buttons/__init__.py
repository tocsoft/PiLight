import math
import automationhat
import time
import threading

_state = [
    0,
    0,
    0
]_lastState = [
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
    global _state
    global _lastState
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
            if current[x] != _lastState[x]:
                _lastChanged[x] = currentTime
            if (currentTime - _lastChanged[x]) > _debounceLimit :
                if current[x] != _state[x]:
                    _state[x] = current[x]
                    if(_state[x] == 1):
                        # changed from unpressed to 0
                        _downTime[x] = currentTime
                        _upTime[x] = 0
                        _eventWaiting[x] = 1
                    else:
                        _upTime[x] = 1
            if _eventWaiting[x] :
                if _upTime[x] == 0: # we are holding down
                    if _downTime[x] > _longPressLimit :
                        triggerEvent(x, 'longPress')
                else:
                    triggerEvent(x, 'press')
        _lastState = current

def triggerEvent(button, event):
    global _eventWaiting
    _eventWaiting[x] = 0
    if event == 'longPress':
        if _longPressCallBacks[button] != None:
            _longPressCallBacks[button](button, event)
    else:
        if _shortPressCallBacks[button] != None:
            _shortPressCallBacks[button](button, event)

_longPressCallBacks = [
    None,None,None
]
_shortPressCallBacks = [
    None,None,None
]

def onLongPress(button, callBack):
    _longPressCallBacks[button] = callBack
def onShortPress(button, callBack):
    _shortPressCallBacks[button] = callBack

_thread = threading.Thread(target=_loop, args=())
_thread.start()