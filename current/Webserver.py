# ...

import RPi.GPIO as GPIO
import json
from flask import Flask, render_template, request
app = Flask(__name__)

P_DILDO = 12 # adapt to your wiring
fPWM = 50  # Hz (not higher with software PWM)
global pwm
GPIO.setmode(GPIO.BOARD)
GPIO.setup(P_DILDO, GPIO.OUT)
pwm = GPIO.PWM(P_DILDO, fPWM)
pwm.start(0)

with open('./templates/config.json', 'r') as f:
     config = json.load(f)

@app.route("/")
def main():
   return render_template('main.html')

@app.route("/new.html")
def new():
   return render_template('index_new.html')   

@app.route("/jquery.min.js")
def jquery():
   return render_template('jquery.min.js')

@app.route("/config.json")
def conf():
   return render_template('config.json')


@app.route('/Level/<duty>')
def pin_state(duty):
    config['newduty'] = float(duty)
    if config['newduty'] <= 0:
       config['newduty'] = 0
    if config['currentduty'] != config['newduty']:
       config['currentduty'] = config['newduty']
    pwm.ChangeDutyCycle(config['currentduty'])
    config['dutytext'] = str(config['currentduty'])
    message = "Dildo is at " + config['dutytext'] + "%"
    with open ('./templates/config.json', 'w') as f:
         json.dump(config, f)
    return message

@app.route('/getLevel.html')
def getLevel():
   response = config['dutytext']
   return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
