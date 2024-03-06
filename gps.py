import math
import threading
import time
import serial

# Puerto

serialPort = 'COM6'
bitTimeOut = 1
bauds = 4800
parity = serial.PARITY_NONE
control_flujo = 1

# Datos para conversion

HUSO = 30
e2 = 0.00669437999013  # excentricidad^2
f = 1 / 298.25722  # achatamiento
re = 6378137  # ecuador
rPc = 6399593.626  # radio polar


def convertir_a_grados(grados, minutos):
    minutos = minutos / 60.0
    return grados + minutos


def convertir_a_radianes_signo(grados, letra):
    rad = math.radians(grados)

    if letra == 'W' or letra == 'S':
        rad = -rad
    return rad


def Proyeccion(HUSO, re, e2, radLon, radLat):
    lambda0 = (HUSO * 6 - 183) * math.pi / 180
    excentricidad = e2 / (1 - e2)
    N = re / (math.sqrt(1 - e2 * math.sin(radLat) * math.sin(radLat)))
    T = math.tan(radLat) * math.tan(radLat)
    C = excentricidad * math.cos(radLat) * math.cos(radLat)
    A = math.cos(radLat) * (radLon - lambda0)
    M = re * ((1 - e2 / 4 - 3 / 64 * math.pow(e2, 2) - 5 / 256 * math.pow(e2, 3)) * radLat
              - (3 / 8 * e2 + 3 / 32 * math.pow(e2, 2) + 45 / 1024 * math.pow(e2, 3)) * math.sin(2 * radLat)
              + (15 / 256 * math.pow(e2, 2) + 45 / 1024 * math.pow(e2, 3)) * math.sin(4 * radLat)
              - (35 / 3072 * math.pow(e2, 3)) * math.sin(6 * radLat))

    UTM_Easting = 0.9996 * N * (A + ((1 - T + C) * A * A * A) / 6 + (
            (5 - 18 * T + T * T + 72 * C - 58 * e2) * math.pow(A, 5)) / 120) + 500000

    UTM_Norting = 0.9996 * (M + N * math.tan(radLat) * (
            ((A * A) / 2) + (((5 - T + 9 * C + 4 * C * C) * math.pow(A, 4)) / 24) + (
            ((61 - 58 * T + T * T + 600 * C - 330 * e2) * math.pow(A, 6)) / 720)))
    return UTM_Norting, UTM_Easting


class Observer:

    def __init__(self, name):
        self.x = -1
        self.y = -1
        self.name = name

    def update(self, linearecibida):
        listvalores = linearecibida.split(',')[2:6]
        latGrados = float(listvalores[0][0:2])
        latMinutos = float(listvalores[0][2::])
        latLetra = listvalores[1]
        longGrados = float(listvalores[2][0:3])
        longMinutos = float(listvalores[2][3::])
        longLetra = listvalores[3]

        self.x, self.y = Proyeccion(HUSO, re, e2,
                                    convertir_a_radianes_signo(grados=convertir_a_grados(longGrados, longMinutos),
                                                      letra=longLetra),
                                    convertir_a_radianes_signo(grados=convertir_a_grados(latGrados, latMinutos),
                                                      letra=latLetra))

        print(linearecibida)
        print("UTM North : " + str(self.x))
        print("UTM East : " + str(self.y))


class filtroSerial:

    def __init__(self, serial):
        self.observers = []
        t = MyThread(serial, self)
        t.start()

    def add_observers(self, observer):
        self.observers.append(observer)
        return self

    def remove_observer(self, observer):
        self.observers.remove(observer)
        return self

    def notify(self, msg):
        for observer in self.observers:
            observer.update(msg)


class MyThread(threading.Thread):
    def __init__(self, ser, subs):
        threading.Thread.__init__(self)
        self.ser = ser
        self.subs = subs

    def run(self):
        self.fserial()

    def fserial(self):
        while self.ser.is_open:
            if ser.inWaiting() > 0:
                line = str(ser.readline())
                if line.split(',')[0] == "b'$GPGGA":
                    if line.split(',')[6] == '0':
                        print("No GPS signal")
                    else:
                        self.subs.notify(line)
                    time.sleep(0.3)


# iniciar

try:
    ser = serial.Serial(serialPort, 4800, timeout=bitTimeOut,
                        parity=parity, rtscts=control_flujo)
    ser.reset_input_buffer()

    subs = filtroSerial(ser)
    obs = Observer('Observador')

    subs.add_observers(obs)

except:
    print("Unkown error")
