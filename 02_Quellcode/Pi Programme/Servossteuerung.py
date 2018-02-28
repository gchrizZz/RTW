import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
pwm.start(0)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
pwm1=GPIO.PWM(13, 50)
pwm1.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)


def SetAngle1(angle1):
    duty = angle1 / 18 + 2
    GPIO.output(13, True)
    pwm1.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(13, False)
    pwm1.ChangeDutyCycle(0)

#SetAngle links
SetAngle(40)
SetAngle(120)


#SetAngle rechts
SetAngle1(120)
SetAngle1(25)

#SetAngle(175)
#68 richtig 0 165np links
#40np // 205

pwm.stop()
pwm1.stop()
GPIO.cleanup()
