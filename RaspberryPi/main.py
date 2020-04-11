#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify
import lights
import buzzer
import buttons
import announcer


app = Flask(__name__)

lastLightAction = None

@app.route('/')
def index():
    global paused
    return jsonify(
        red=bool(lights.getLight(0)),
        amber=bool(lights.getLight(1)),
        green=bool(lights.getLight(2)),
        paused=bool(paused),
        sound=bool(buzzer.sounding())
    )

@app.route('/light/red')
def toggleRed():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    if lastLightAction != flashRed:
        lastLightAction = toggleRed    
    if paused == False:
        lights.start([[1,0,0]])
    return 'red'

@app.route('/flash/red')
def flashRed():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    lastLightAction = flashRed
    # flash twice then show solid red
    if paused == False:
        lights.start([[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5]], toggleRed)
    return 'red-flash'

@app.route('/light/amber')
def toggleAmber():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    if lastLightAction != flashamber:
        lastLightAction = toggleAmber
    if paused == False:
        lights.start([[0,1,0]])
    return 'amber'

@app.route('/flash/amber')
def flashamber():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    lastLightAction = flashamber
    if paused == False:
        lights.start([[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5]],toggleAmber )
    return 'amber-flash'

@app.route('/light/green')
def toggleGreen():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    if lastLightAction != flashgreen:
        lastLightAction = toggleGreen
    if paused == False:
        lights.start([[0,0,1]])
    return 'green'

@app.route('/flash/green')
def flashgreen():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    lastLightAction = flashgreen
    if paused == False:
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
    global paused
    if request.args.get('force'):
        paused = False
    lastLightAction = toggleStrobe
    if paused == False:
        lights.start([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
    return 'strobe'

@app.route('/light/bounce')
def toggleBounce():
    global lastLightAction
    global paused
    if request.args.get('force'):
        paused = False
    lastLightAction = toggleBounce
    if paused == False:
        lights.start([[1,0,0,0.5],[0,1,0,0.25],[0,0,1,0.5],[0,1,0,0.25]])
    return 'strobe'

@app.route('/sound')
def makeSound():
    global paused
    if request.args.get('force'):
        paused = False
    if paused == False:
        buzzer.start(pattern=[[1,0.25],[0,0.5]], loopCounter=5)
    return 'strobe'

@app.route('/sound/forever')
def makeSoundForverer():
    global paused
    if request.args.get('force'):
        paused = False
    if paused == False:
        buzzer.start(pattern=[[1,0.25],[0,0.25]])
    return 'strobe'

@app.route('/mute')
def mute():
    buzzer.stop()
    return 'muted'
    
@app.route('/pause')
def pause():
    global lastLightAction    
    global paused
    print ("pausing")
    paused  = True
    lights.stop()
    return 'paused'
        
@app.route('/unpause')
def unpause():
    global lastLightAction    
    global paused
    if paused:
       paused = False
       lastLightAction()
    return 'unpaused'

paused = False
def buttonLongPress(button, event):
    print ("long press")
    global lastLightAction    
    global paused
    if paused:
       paused = False
       lastLightAction()
    else :
        if lastLightAction != None:
            print ("pausing")
            paused  = True
            lights.stop()
        else:
            wakeUpFlash()

lightOn = 0
def buttonPress(button, event):
    global paused
    global lightOn
    paused = False
    if buzzer.sounding():
        mute()
    else:
        lightOn = lightOn + 1
        lightOn = lightOn % 4
        if lightOn == 0:
            toggleAllOff()
        if lightOn == 1:
            toggleRed()
        if lightOn == 2:
            toggleAmber()
        if lightOn == 3:
            toggleGreen()
    print ("press")

def wakeUpFlash():
    lights.start([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]], loopCounter=1)
    
if __name__ == '__main__':
    
    buttons.onShortPress(0, buttonPress)
    buttons.onLongPress(0, buttonLongPress)

    buzzer.stop()
    wakeUpFlash()
    announcer.start()
    app.run(host='0.0.0.0', port=80)