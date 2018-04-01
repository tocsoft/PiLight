import math
import automationhat
import time
import threading


_currentState = 0
_sounder = automationhat.relay.one

_offPattern = [[0]]

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
    global _loopEnabled
    while True:
        if _run:
            entry = _pattern[_patternIndex]
            _set(entry[0])
            
            if(len(entry) == 2):
                time.sleep(entry[1])

            _patternIndex +=1
            if (len(_pattern) == _patternIndex):
                _patternIndex = 0
                if (_loopEnabled):
                    _loopPos += 1
                    if(_loopPos >= _loopCounter):
                        _tryEndLoop()
                else:
                    _tryEndLoop()

def _tryEndLoop():
    global _callBack
    if (_callBack is not None):            
        if (_callBack()):
            _loopPos = 0
        else:
            stopPattern()
    else:
        stopPattern()

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
    global _loopCounter
    global _run
    _set(0)
    _run = False
    
def setPattern(pattern, callBack = None, loopCounter = -1):
    global _patternIndex
    global _pattern
    global _loopCounter
    global _run
    global _callBack
    stopPattern()
    _callBack = callBack
    _loopCounter = loopCounter
    _pattern = pattern
    _patternIndex= 0
    _loopPos = 0
    _loopEnabled = (loopCounter > 0)
    _run = True
    


_thread = threading.Thread(target=_loop, args=())
_thread.start()