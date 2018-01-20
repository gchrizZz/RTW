"""Hier können wir uns mit dem Quellcode unseres CopterAutos austoben"""
""" benötigte Funktionen:

Start (nach start flifla)
Fahren
Stoppen
hochfliegen
vorfliegen
Landen
Zielerkennung/anfliegen
Ende
Drohne stabilisieren
FliFa (fliegen->fahren)
FaFli (fahren ->fliegen)

Wasserausweichen


(Datenaustausch)
(Ausweichen)
(Notaus)
"""
Astand:
  # coding=utf-8
# Benötigte Module werden eingefügt und konfiguriert
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
 
# Hier können die jeweiligen Eingangs-/Ausgangspins ausgewählt werden
Trigger_AusgangsPin = XX
Echo_EingangsPin    = XX
 
# Die Pause zwischen den einzelnen Messugnen kann hier in Sekunden eingestellt werden
sleeptime = 0.8
 
# Hier werden die Ein-/Ausgangspins konfiguriert
GPIO.setup(Trigger_AusgangsPin, GPIO.OUT)
GPIO.setup(Echo_EingangsPin, GPIO.IN)
GPIO.output(Trigger_AusgangsPin, False)
 
# Hauptprogrammschleife
try:
    while True:
        # Abstandsmessung wird mittels des 10us langen Triggersignals gestartet
        GPIO.output(Trigger_AusgangsPin, True)
        time.sleep(0.00001)
        GPIO.output(Trigger_AusgangsPin, False)
 
        # Hier wird die Stopuhr gestartet
        EinschaltZeit = time.time()
        while GPIO.input(Echo_EingangsPin) == 0:
            EinschaltZeit = time.time() # Es wird solange die aktuelle Zeit gespeichert, bis das Signal aktiviert wird
 
        while GPIO.input(Echo_EingangsPin) == 1:
            AusschaltZeit = time.time() # Es wird die letzte Zeit aufgenommen, wo noch das Signal aktiv war
 
        # Die Differenz der beiden Zeiten ergibt die gesuchte Dauer
        Dauer = AusschaltZeit - EinschaltZeit
        # Mittels dieser kann nun der Abstand auf Basis der Schallgeschwindigkeit der Abstand berechnet werden
        Abstand = (Dauer * 34300) / 2
 
        
        # Pause zwischen den einzelnen Messungen
        time.sleep(sleeptime)
      if Abstand > 30:
        Fahren()
      elif Abstand < 30:
        Stoppen()
        FaFli()
        Hochfliegen()
        Vorfliegen()
        Landen()
        FliFa()
        Fahren()
      else:
        Fahren()
 
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()
