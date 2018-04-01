
import automationhat
import time
import threading


_redLight = 0
_amberLight = 1
_greenLight = 2

_offPattern = [[0,0,0]]

_pattern = _offPattern
_patternIndex = 0 
_callBack = None

def _animateLoop():
    global _patternIndex
    global _pattern
    global _callBack
    while True:
        _patternIndex = _patternIndex % len(_pattern)
        entry = _pattern[_patternIndex]
        _setLight(0, entry[0])
        _setLight(1, entry[1])
        _setLight(2, entry[2])
        if(len(entry) == 4):
            time.sleep(entry[3])

        _patternIndex +=1
        if (len(_pattern) == _patternIndex):
            if (_callBack is not None):            
                if (_callBack()):
                    _patternIndex = 0
                else:
                    stopAnimation()

def _setLight(light, state):
    light = light % 3
    if light == 0:
        automationhat.output.one.on(state)
    if light == 1:
        automationhat.output.two.write(state)
    if light == 2:
        automationhat.output.three.write(state)

def allOff():
    stopAnimation()

def stopAnimation():
    global _patternIndex
    global _pattern
    global _callBack
    _callBack = None
    _pattern = _offPattern
    _patternIndex= 0
    _setLight(0,0)
    _setLight(1,0)
    _setLight(2,0)
    
def setAnimation(pattern, callBack = None):
    global _patternIndex
    global _pattern
    global _callBack
    stopAnimation()
    _callBack = callBack
    _pattern = pattern
    _patternIndex= 0




_thread = threading.Thread(target=_animateLoop, args=())
_thread.start()