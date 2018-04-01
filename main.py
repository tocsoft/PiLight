#!/usr/bin/env python3

from flask import Flask
import lights
import buzzer


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'


@app.route('/light/red')
def toggleRed():
    lights.setAnimation([[1,0,0]])
    return 'red'

@app.route('/flash/red')
def flashRed():
    # flash twice then show solid red
    lights.setAnimation([[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5],[1,0,0,0.5],[0,0,0,0.5]], toggleRed)
    return 'red-flash'

@app.route('/light/amber')
def toggleAmber():
    lights.setAnimation([[0,1,0]])
    return 'amber'

@app.route('/flash/amber')
def flashamber():
    lights.setAnimation([[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5],[0,1,0,0.5],[0,0,0,0.5]],toggleAmber )
    return 'amber-flash'

@app.route('/light/green')
def toggleGreen():
    lights.setAnimation([[0,0,1]])
    return 'green'

@app.route('/flash/green')
def flashgreen():
    lights.setAnimation([[0,0,0,0.5],[0,0,1,0.5],[0,0,0,0.5],[0,0,1,0.5],[0,0,0,0.5]],toggleGreen)
    return 'green-flash'
    
@app.route('/light/off')
def toggleAllOff():
    lights.allOff()
    return 'all off'

@app.route('/light/strobe')
def toggleStrobe():
    lights.setAnimation([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
    return 'strobe'

@app.route('/sound')
def makeSound():
    buzzer.setPattern(pattern=[[1,0.25],[0,0.5]], loopCounter=5)
    return 'strobe'

@app.route('/sound/forever')
def makeSoundForverer():
    buzzer.setPattern(pattern=[[1,0.25],[0,0.25]], loopCounter=-1)
    return 'strobe'

@app.route('/mute')
def mute():
    buzzer.off()
    return 'muted'

def _finishedStrobe():
    lights.allOff()  

buzzer.off()
lights.allOff()
lights.setAnimation([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]], _finishedStrobe)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)