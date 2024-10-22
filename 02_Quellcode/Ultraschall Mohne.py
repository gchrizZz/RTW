import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  #Servo1
pwm=GPIO.PWM(11, 50)
pwm.start(0)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
pwm1=GPIO.PWM(7, 50)        #Servo2
pwm1.start(0)

GPIO.setup(10,GPIO.OUT) #Propeller1
GPIO.setup(11,GPIO.out) #Propeller2

GPIO_TRIGGER = 18       #Ultraschall
GPIO_ECHO = 24          #Ultraschall
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distanz():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)


def SetAngle1(angle1):
    duty = angle1 / 18 + 2
    GPIO.output(7, True)
    pwm1.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(7, False)
    pwm1.ChangeDutyCycle(0)





#SetAngle links
    #SetAngle(40)
    #SetAngle(125)
#SetAngle rechts
    #SetAngle1(110)
    #SetAngle1(25)

#SetAngle(175)
#68 richtig 0 165np links
#40np // 205
if __name__ == '__main__':
    try:
        while True:
            abstand = distanz()
            #print("Gemessene Entfernung = %.1f cm" % abstand)
            #time.sleep(1)
            SetAngle(40)
            SetAngle1(110)
            #Motor an 10 11
            GPIO.output(10,1)
            GPIO.output(11,1)
            if abstand < 40:
                #motor aus
                GPIO.output(10,0)
                GPIO.output(11,0)
                SetAngle(125)
                SetAngle1(25)
                pwm.stop()
                pwm1.stop()


            # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
#pwm.stop()
#pwm1.stop()
GPIO.cleanup()

