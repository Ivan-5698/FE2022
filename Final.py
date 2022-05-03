import cv2
import RobotAPI as rapi
import numpy as np
import serial
import time

port = serial.Serial("/dev/ttyS0", baudrate=115200, stopbits=serial.STOPBITS_ONE)
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

message = ""
ii = ""
fps = 0
fps1 = 0
fps_time = 0
state = 0
speed =0

flag_or = 0
flag_bo = 0

flag_gr = 0
flag_rd = 0

pov = 0
blue = 0
orange = 0

rul = 1500
sp = 0
sr1 = 0
sr2 = 0
e = 0
kp = 10
kd = 10
timer11=time.time()

u=0
e_old=0

xb1, yb1 = 620,200
xb2, yb2 = 640,480

xbs1, ybs1 = 0,200
xbs2, ybs2 = 20,480

def black_line():
    global xb1, yb1, xb2, yb2, sr1, frame, xbs1, ybs1, xbs2, ybs2, sr2
    datb1 = frame[yb1:yb2, xb1:xb2]
    datb2 = frame[ybs1:ybs2, xbs1:xbs2]

    hsv1 = cv2.cvtColor(datb1, cv2.COLOR_BGR2GRAY)
    ret, maskd1 = cv2.threshold(hsv1, 70, 255, cv2.THRESH_BINARY_INV)

    imd1, contoursd1, hod1 = cv2.findContours(maskd1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sr1 = 0

    for contorb1 in contoursd1:
        x, y, w, h = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 400:
            if y + h > sr1:
                sr1 = y + h
            cv2.rectangle(datb1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    hsv2 = cv2.cvtColor(datb2, cv2.COLOR_BGR2GRAY)
    ret, maskd2 = cv2.threshold(hsv2, 70, 255, cv2.THRESH_BINARY_INV)

    imd2, contoursd2, hod2 = cv2.findContours(maskd2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sr2 = 0

    for contorb2 in contoursd2:
        x, y, w, h = cv2.boundingRect(contorb2)
        a2 = cv2.contourArea(contorb2)
        if a2 > 400:
            if y + h > sr2:
                sr2 = y + h
            cv2.rectangle(datb2, (x, y), (x + w, y + h), (0, 255, 0), 2)


    cv2.rectangle(frame, (xb1, yb1), (xb2, yb2), (0, 0, 255), 2)
    cv2.rectangle(frame, (xbs1, ybs1), (xbs2, ybs2), (0, 0, 255), 2)



xbo1, ybo1 = 270,390
xbo2, ybo2 = 370,430

lowb = np.array([72,70,65])
upb = np.array([111, 255, 200])

lowo = np.array([12,65,90])
upo = np.array([75, 255, 255])


def blue_orange():
    global xbo1, ybo1, xbo2, ybo2, frame, blue, orange

    orange = 0
    blue = 0

    datb1 = frame[ybo1:ybo2, xbo1:xbo2]

    datB = cv2.GaussianBlur(datb1, (5, 5), cv2.BORDER_DEFAULT)
    hsvB = cv2.cvtColor(datB, cv2.COLOR_BGR2HSV)
    maskdB = cv2.inRange(hsvB, lowb, upb)
    imdB, contoursdB, hodB = cv2.findContours(maskdB, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contorb1 in contoursdB:
        x, y, w, h = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 50:
            blue = 1
            cv2.rectangle(datb1, (x, y), (x + w, y + h), (255, 0, 0), 2)


    datO = cv2.GaussianBlur(datb1, (5, 5), cv2.BORDER_DEFAULT)
    hsvO = cv2.cvtColor(datO, cv2.COLOR_BGR2HSV)
    maskdO = cv2.inRange(hsvO, lowo, upo)
    imdO, contoursdO, hodO = cv2.findContours(maskdO, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contorb1 in contoursdO:
        x, y, w, h = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 50:
            orange = 1
            cv2.rectangle(datb1, (x, y), (x + w, y + h), (0, 0, 255),2)

    cv2.rectangle(frame, (xbo1, ybo1), (xbo2, ybo2), (0, 255, 0),2)



xgr1, ygr1 = 30,200
xgr2, ygr2 = 610,380

lowg = np.array([45, 101, 49])
upg = np.array([81, 255, 103])

lowr = np.array([0, 98, 0])
upr = np.array([8, 255, 255])


def green_red():
    global xgr1, ygr1, xgr2, ygr2, frame, green, red

    red = 0
    green = 0

    datb1 = frame[ygr1:ygr2, xgr1:xgr2]

    datB = cv2.GaussianBlur(datb1, (5, 5), cv2.BORDER_DEFAULT)

    hsvB = cv2.cvtColor(datB, cv2.COLOR_BGR2HSV)
    maskdB = cv2.inRange(hsvB, lowg, upb)
    imdB, contoursdB, hodB = cv2.findContours(maskdB, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contorb1 in contoursdB:
        x, y, w, h = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 50:
            green = 1
            cv2.rectangle(datb1, (x, y), (x + w, y + h), (255, 0, 0), 2)


    datO = cv2.GaussianBlur(datb1, (5, 5), cv2.BORDER_DEFAULT)
    hsvO = cv2.cvtColor(datO, cv2.COLOR_BGR2HSV)
    maskdO = cv2.inRange(hsvO, lowr, upr)
    imdO, contoursdO, hodO = cv2.findContours(maskdO, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contorb1 in contoursdO:
        x, y, w, h = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 50:
            red = 1
            cv2.rectangle(datb1, (x, y), (x + w, y + h), (0, 0, 255),2)

    cv2.rectangle(frame, (xgr1, ygr1), (xgr2, ygr2), (0, 255, 0),2)

while 1:
    frame = robot.get_frame(wait_new_frame=1)

    fps1 += 1
    if time.time() > fps_time + 1:
        fps_time = time.time()
        fps = fps1
        fps1 = 0

    if state == 0:
        message = '9999999$'
        if ii == 'B=0':
            state = 2

    if state == 1:
        key = robot.get_key()
        sp += 1
        if key != -1:
            sp = 0
            if key == 87:
                speed = 20
            if key == 83:
                speed = -20
            if key == 65: #налево
                rul += 10
            if key == 68: #направо
                rul -= 10

        if sp > 10:
            speed = 0

        message = str(speed + 200) + str(rul + 1000) + '$'

    if state == 2:
        black_line()
        blue_orange()
        green_red()

        if green == 1:
            e = sr2 - sr1 - 30
        elif red == 1:
            e = sr2 - sr1 - 30
        else:
            e = sr2-sr1-30

        u = e * kp + (e - e_old) * kd
        deg = int(rul - u)
        e_old=e
        if sr1 == 0:
            deg = 0
        if sr2 == 0:
            deg = 4000

        if flag_bo == 0 and flag_or == 0:
            if blue == 1:
                flag_bo = 1
            if orange == 1:
                flag_or = 1

        if flag_bo == 1 and timer11 + 0.5 < time.time() and blue == 1:
            pov += 1
            timer11 = time.time()

        if flag_or == 1 and timer11 + 0.5 < time.time() and orange == 1:
            pov += 1
            timer11 = time.time()

        if pov == 12:
            state = 3
            timer11 = time.time()

        message = str(speed + 200) + str(deg + 1000) + '$'


    if state == 3:
        if timer11 + 0.4 > time.time():
            black_line()
            e = sr2 - sr1 - 30
            u = e * kp + (e - e_old) * kd
            deg = rul - u
            e_old = e
            if sr1 == 0:
                deg = 0
            if sr2 == 0:
                deg = 4000
        else:
            speed = 0
            deg = rul

        message = str(speed + 200) + str(deg + 1000) + '$'

    port.write(message.encode("utf-8"))




    if port.in_waiting > 0:
        ii = ""
        t = time.time()
        while 1:
            a = str(port.read(), "utf-8")
            if a != '$':
                ii += a
            else:
                break
            if t + 0.02 < time.time():
                break
        port.reset_input_buffer()


    robot.text_to_frame(frame, 'm = ' + message + '   but = ' + ii + ' state = ' + str(state) , 20, 20)
    robot.text_to_frame(frame, 'd1 = ' + str(sr1)  + '   d2 = ' + str(sr2)  + ' e = ' +  str(e) + ' pov = ' +  str(pov), 20, 40)
    robot.text_to_frame(frame,  'fb = ' + str(flag_bo) + '   fo = ' + str(flag_or)+ '   b = ' + str(blue)+ '   o = ' + str(orange), 20, 60)
    robot.text_to_frame(frame, 'fps = ' + str(fps), 500, 20)
    robot.set_frame(frame, 40)