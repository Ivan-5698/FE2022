from pyb import delay, Pin, ADC, Timer, UART
import pyb
uart = UART(6, 115200, stop=1)
message = "123$"
inn = ''
serv_deg = ADC("X4")

pic = Pin('Y10', Pin.OUT_PP)
# p_out.high()
# p_out.low()

button = Pin('Y9', Pin.IN, Pin.PULL_UP)
# p_in.value()


M1 = Pin('X5', Pin.OUT_PP)
M2 = Pin('X6', Pin.OUT_PP)
MS = Pin('X10')
tim = Timer(4, freq = 10000)
ch = tim.channel(2, Timer.PWM, pin = MS)

S1 = Pin('X7', Pin.OUT_PP)
S2 = Pin('X8', Pin.OUT_PP)
SS = Pin('X9')
tim = Timer(4, freq = 10000)
chS = tim.channel(1, Timer.PWM, pin = SS)

def Motor(sp):
    global ch, M1, M2
    if sp < 0:
        M1.low()
        M2.high()
        sp = -sp

    else:
        M2.low()
        M1.high()
    ch.pulse_width_percent(sp)

eold = 0

def Serv(deg): # управление сервой(пд регулятор)
    global eold, S1, S2, chS
    if deg < 450:
        deg = 450
    if deg > 2990:
        deg = 2990
    e = serv_deg.read() - deg # ошибка
    u = e * 0.1 + (e - eold)*0.3 # скорость
    if u < 0:
        S1.low()
        S2.high()
        u = -u
    else:
        S2.low()
        S1.high()
    if u > 100:
        u = 100
    if u < 5:
        u = 15
    if -50< e < 50:
        u = 0
        S1.low()
        S2.low()
    chS.pulse_width_percent(u)
    eold = e

flag_start = True
speed = 0
rul = 0
flag =1


while True:
    if flag == 1:
        Motor(0)
        Serv(1800)
    #print(serv_deg.read()) # 780 , 3027, 2112

    if uart.any():
        a = chr(uart.readchar())
        if a != '$':
            inn += a
            if len(inn) > 9:
                inn = ""
        else:
            if flag_start:
                if inn == "9999999":
                    flag_start = False
                    pic.high()
                    delay(500)
                    pic.low()
                    flag = 0
            else:
                message = 'B=' + str(button.value()) + '$'
                try:
                    if len(inn) == 7 and inn != '9999999':
                        speed = int(inn[:3])-200
                        rul = int(inn[3:])-1000
                        print(speed, rul)
                        Motor(speed)
                        Serv(rul)
                except ValueError:
                    print("err")

            # print(inn)
            inn = ""
            uart.write(message)
