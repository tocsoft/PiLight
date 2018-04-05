#!/usr/bin/env python3

from flask import Flask
import lights
import buzzer
import buttons
import announcer


app = Flask(__name__)

lastLightAction = None

@app.route('/')
def index():
    return 'Hello world'

@app.route('/light/red')
def toggleRed():
    global lastLightAction
    if lastLightAction != flashRed:
        lastLightAction = toggleRed

    lights.start([[1,0,0]])
    return 'red'

@app.route('/flash/red')
def flashRed():
    global lastLightAction
    lastLightAction = flashRed
    # flash twice then show solid red
    lights.start([[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5]], toggleRed)
    return 'red-flash'

@app.route('/light/amber')
def toggleAmber():
    global lastLightAction
    if lastLightAction != flashamber:
        lastLightAction = toggleAmber
    lights.start([[0,1,0]])
    return 'amber'

@app.route('/flash/amber')
def flashamber():
    global lastLightAction
    lastLightAction = flashamber
    lights.start([[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5]],toggleAmber )
    return 'amber-flash'

@app.route('/light/green')
def toggleGreen():
    global lastLightAction
    if lastLightAction != flashgreen:
        lastLightAction = toggleGreen
    lights.start([[0,0,1]])
    return 'green'

@app.route('/flash/green')
def flashgreen():
    global lastLightAction
    lastLightAction = flashgreen
    lights.start([[0,0,0,0.5],[0,0,1,0.5],[0,0,0,0.5],[0,0,1,0.5],[0,0,0,0.5]],toggleGreen)
    return 'green-flash'
    
@app.route('/light/off')
def toggleAllOff():
    lastLightAction = None
    lights.stop()
    return 'all off'

@app.route('/light/strobe')
def toggleStrobe():
    global lastLightAction
    lastLightAction = toggleStrobe
    lights.start([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
    return 'strobe'

@app.route('/light/bounce')
def toggleBounce():
    global lastLightAction
    lastLightAction = toggleBounce
    lights.start([[1,0,0,0.5],[0,1,0,0.25],[0,0,1,0.5],[0,1,0,0.25]])
    return 'strobe'

@app.route('/sound')
def makeSound():
    buzzer.start(pattern=[[1,0.25],[0,0.5]], loopCounter=5)
    return 'strobe'

@app.route('/sound/forever')
def makeSoundForverer():
    buzzer.start(pattern=[[1,0.25],[0,0.25]])
    return 'strobe'

@app.route('/mute')
def mute():
    buzzer.stop()
    return 'muted'

paused = False
def buttonLongPress(button, event):
    print ("long press")
    global lastLightAction    
    global paused
    if paused:
       lastLightAction()
       paused = False
    else :
        if lastLightAction != None:
            print ("pausing")
            paused  = True
            lights.stop()
        else:
            wakeUpFlash()
    
def buttonPress(button, event):
    print ("press")
    mute()

def wakeUpFlash():
    lights.start([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]], loopCounter=1)
    
if __name__ == '__main__':
    
    buttons.onShortPress(0, buttonPress)
    buttons.onLongPress(0, buttonLongPress)

    buzzer.stop()
    wakeUpFlash()
    announcer.start()
    app.run(host='0.0.0.0', port=80)