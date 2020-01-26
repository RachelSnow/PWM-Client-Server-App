#!/usr/bin/env python

import logging
import logging.handlers
import argparse
import sys
# import time  # this is only being used as part of the example
import os
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

# Deafults
LOG_FILENAME = "/tmp/myservice.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

with open('./templates/config.json', 'r') as f:
     config = json.load(f)

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
	def __init__(self, logger, level):
		"""Needs a logger and a logger level."""
		self.logger = logger
		self.level = level

	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

i = 0

# Loop forever, doing something useful hopefully:
while True:
@app.route("/")
def main():
   return render_template('main.html')

@app.route("/test.html")
def test():
   return render_template('test.html')

@app.route("/test2.html")
def test2():
   return render_template('test2.html')

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