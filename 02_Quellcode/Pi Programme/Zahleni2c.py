import smbus
import time
bus = smbus.SMBus(1)

address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number

while True:
    senden = input("Zahl zwischen 1 - 9: ")
    if not senden:
        continue

    writeNumber(int(senden))
    print ("Raspberry Schickt folgende Zahl: ", senden)
    time.sleep(1)

    empfang = readNumber()
    print ("Der Arduino empfengt/schickt folgende Zahl: ", empfang)
