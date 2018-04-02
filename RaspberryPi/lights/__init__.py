
import automationhat
import time
import threading


_currentState = [0,0,0]
_lights = [
    automationhat.output.one,
    automationhat.output.two,
    automationhat.output.three
]

_offPattern = [[0,0,0]]

_pattern = _offPattern
_patternIndex = 0 
_loopCounter = -1
_loopPos = 0
_callBack = None
_run = False
_loopEnabled  = False


def _loop():
    global _patternIndex
    global _run
    global _pattern
    global _callBack
    global _loopCounter
    global _loopPos
    global _loopEnabled
    
    while True:
        if _run:
            entry = _pattern[_patternIndex]
            _setLight(0, entry[0])
            _setLight(1, entry[1])
            _setLight(2, entry[2])
            
            if(len(entry) == 4):
                time.sleep(entry[3])

            _patternIndex +=1
            if (len(_pattern) == _patternIndex):
                _patternIndex = 0
                if (_loopEnabled):
                    _loopPos += 1
                    if(_loopPos >= _loopCounter):
                        _loopPos = 0
                        if (_callBack is not None):            
                            _callBack() # callback is responsible for calling stop after loop count completed
                        else:
                            stop()
                else:
                    # loop forever unless callback stops it
                    if (_callBack is not None):            
                        _callBack()
          
def _setLight(light, state, force=False):
    light = light % 3
    global _currentState
    global _lights
    if(_currentState[light] != state) or (force == True):
        _lights[light].write(state)
        _currentState[light] = state

def stop():
    global _run
    _setLight(0,0, True)
    _setLight(1,0, True)
    _setLight(2,0, True)
    _run = False
    
def start(pattern, callBack = None, loopCounter = -1):
    global _patternIndex
    global _pattern
    global _loopCounter
    global _run
    global _callBack
    global _loopEnabled
    global _loopPos
    stop()
    _callBack = callBack
    _loopCounter = loopCounter
    _pattern = pattern
    _patternIndex= 0
    _loopPos = 0
    _loopEnabled = (_loopCounter > 0)
    _run = True



_thread = threading.Thread(target=_loop, args=())
_thread.start()