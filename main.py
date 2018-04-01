#!/usr/bin/env python3

from flask import Flask
import lights
import buzzer
import announcer


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'


@app.route('/light/red')
def toggleRed():
    lights.start([[1,0,0]])
    return 'red'

@app.route('/flash/red')
def flashRed():
    # flash twice then show solid red
    lights.start([[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5]], toggleRed)
    return 'red-flash'

@app.route('/light/amber')
def toggleAmber():
    lights.start([[0,1,0]])
    return 'amber'

@app.route('/flash/amber')
def flashamber():
    lights.start([[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5]],toggleAmber )
    return 'amber-flash'

@app.route('/light/green')
def toggleGreen():
    lights.start([[0,0,1]])
    return 'green'

@app.route('/flash/green')
def flashgreen():
    lights.start([[0,0,0,0.5],[0,0,1,0.5],[0,0,0,0.5],[0,0,1,0.5],[0,0,0,0.5]],toggleGreen)
    return 'green-flash'
    
@app.route('/light/off')
def toggleAllOff():
    lights.stop()
    return 'all off'

@app.route('/light/strobe')
def toggleStrobe():
    lights.start([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
    return 'strobe'

@app.route('/light/bounce')
def toggleBounce():
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

if __name__ == '__main__':
    buzzer.stop()
    lights.start([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]], loopCounter=1)
    announcer.start()
    app.run(host='0.0.0.0', port=80)