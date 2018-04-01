
import automationhat
import time
import threading


_redLight = 0
_amberLight = 1
_greenLight = 2
_thread = threading.Thread(target=_animateLoop, args=())

_offPattern = [[0,0,0]]

_pattern = _offPattern
_patternIndex = 0 
_callBack 

def _animateLoop():
    while True:
        _patternIndex = _patternIndex % len(_pattern)
        entry = _pattern[_patternIndex]
        _setLight(0, entry[0])
        _setLight(1, entry[1])
        _setLight(2, entry[2])
        if(len(entry) == 4):
            time.sleep(entry[3])

        _patternIndex +=1
        if(len(_pattern) == _patternIndex & _callBack):
            if(_callBack()):
                _patternIndex = 0
            else:
                stopAnimation()

def _setLight(light, state):
    light = light % 3
    if light == 0:
        automationhat.output.one.write(state)
    if light == 1:
        automationhat.output.two.write(state)
    if light == 2:
        automationhat.output.three.write(state)

def allOff():
    stopAnimation()

def stopAnimation():
    _callBack = null
    _pattern = _offPattern
    _patternIndex= 0
    _setLight(0,0)
    _setLight(1,0)
    _setLight(2,0)
    
def setAnimation(pattern, callBack):
    stopAnimation()
    _callBack = callBack
    _pattern = pattern
    _patternIndex= 0