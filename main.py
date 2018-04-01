#!/usr/bin/env python3

from flask import Flask
import lights


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
    lights.setAnimation([[1,0,0,0.5],[0,0,0,0.5]])
    return 'red-flash'

@app.route('/light/amber')
def toggleAmber():
    lights.setAnimation([[0,1,0]])
    return 'amber'

@app.route('/flash/amber')
def flashamber():
    lights.setAnimation([[0,1,0,0.5],[0,0,0,0.5]])
    return 'amber-flash'

@app.route('/light/green')
def toggleGreen():
    lights.setAnimation([[0,0,1]])
    return 'green'

@app.route('/flash/green')
def flashgreen():
    lights.setAnimation([[0,0,1,0.5],[0,0,0,0.5]])
    return 'green-flash'
    
@app.route('/light/off')
def toggleAllOff():
    lights.allOff()
    return 'all off'


def _finishedStrobe(i, result):
    lights.allOff()  

lights.setAnimation([[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]], _finishedStrobe)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)