
import automationhat
import time
import threading


_currentState = 0
_sounder = automationhat.relay.one

_offPattern = [[0]]

_pattern = _offPattern
_patternIndex = 0 
_callBack = None

def _loop():
    global _patternIndex
    global _pattern
    global _callBack
    while True:
        if(_patternIndex >= 0):
            entry = _pattern[_patternIndex]
            _set(entry[0])
            if(len(entry) == 2):
                time.sleep(entry[1])

            _patternIndex +=1
            if (len(_pattern) == _patternIndex):
                _patternIndex = 0
                if (_callBack is not None):            
                    if (_callBack()):
                        _patternIndex = 0
                    else:
                        stopAnimation()

def _set(state, force=False):
    global _currentState
    global _sounder
    if(_currentState != state) or (force == True):
        _sounder.write(state)
       _currentState = state

def off():
    stopPattern()
    _set(0, True)

def stopPattern():
    global _patternIndex
    global _pattern
    global _callBack
    _callBack = None
    _patternIndex= -10
    _pattern = _offPattern
    _patternIndex= 0
    _set(0)
    
def setPattern(pattern, callBack = None):
    global _patternIndex
    global _pattern
    global _callBack
    stopPattern()
    _callBack = callBack
    _patternIndex= -10
    _pattern = pattern
    _patternIndex= 0


_thread = threading.Thread(target=_loop, args=())
_thread.start()