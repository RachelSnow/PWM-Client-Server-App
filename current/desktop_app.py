# ...

import Tkinter
import time
import pygame
import urllib2
from urllib2 import urlopen
import json

event = 0
duty = 0

config = {'currentduty': '0','dutytext': '0','newduty': '0'}
with open('./templates/config.json', 'r') as f:
     config = json.load(f)

def joy_do():
    global joyval
    global a_button_val
    global b_buton_val
    pygame.event.pump()
    joyval = (int(myjoystick.get_axis(1)*100))
    a_button_val = (int(myjoystick.get_button(0)))
    b_button_val = (int(myjoystick.get_button(1)))
    if a_button_val == 1:
       decrease_duty(event)
    if b_button_val == 1:
       increase_duty(event)
#    print "joyval =", joyval
    if joyval >= 1:
       increase_duty(event)
    if joyval <= -1:
       decrease_duty(event)
    root.after(100, joy_do)

def read_json():
    global duty
    if duty >= 33:
       duty = 33
    if config['currentduty'] != duty:
       duty = int(config['currentduty'])
    print("duty is {} type {}".format(duty, type(duty)))
    scale.set(duty)
    text.delete('1.0', '1.6')
    text.insert('1.0', duty)


def read_duty(duty):
    config['dutytext'] = str(duty)
    if config['currentduty'] != duty:
       config['currentduty'] = duty
       with open ('./templates/config.json', 'w') as f:
            json.dump(config, f)
    url = "http://127.0.0.1:8080/Level/" + config['currentduty']
    urllib2.urlopen(url).read()
    text.delete('1.0', '1.6')
    text.insert('1.0', duty)
#    print "D =", duty, "%"

def increase_duty(event):
    global duty
    duty += 3
    if duty >= 33:
       duty = 33
    if config['currentduty'] != duty:
       config['currentduty'] = duty
       with open ('./templates/config.json', 'w') as f:
            json.dump(config, f)
    config['dutytext'] = str(duty)
    url = "http://127.0.0.1:8080/Level/" + config['dutytext']
    urllib2.urlopen(url).read()
    text.delete('1.0', '1.6')
    text.insert('1.0', duty)
#    print "D =", duty, "%"

def decrease_duty(event):
    global duty
    duty -= 3
    if duty <= 0:
       duty = 0
    if config['currentduty'] != duty:
       config['currentduty'] = duty
       with open ('./templates/config.json', 'w') as f:
            json.dump(config, f)
    config['dutytext'] = str(duty)
    url = "http://127.0.0.1:8080/Level/" + config['dutytext']
    urllib2.urlopen(url).read()
    text.delete('1.0', '1.6')
    text.insert('1.0', duty)
#    print "D =", duty, "%"

pygame.init()
joystickcount = pygame.joystick.get_count()
if joystickcount > 0:
    myjoystick = pygame.joystick.Joystick(0)
    myjoystick.init()
if joystickcount < 1:
    myjoystick = 0

root = Tkinter.Tk()
root.title( "MOSFET PWM Dildo Demo" )
root.geometry( "420x240" )
scale = Tkinter.Scale(orient='horizontal', from_=0, to=33, width=40, length=4000, command=read_duty)
scale.pack()
up = Tkinter.Button(root, text="+", command= lambda: increase_duty(event))
up.pack()
down = Tkinter.Button(root, text="-", command= lambda: decrease_duty(event))
down.pack()
text = Tkinter.Text(root, height=1, width=16)
text.pack()
root.bind("<Up>", increase_duty)
root.bind("<Down>", decrease_duty)

if joystickcount > 0:
    joy_do()

while True:
    read_json()
    root.update_idletasks()
    root.update()
