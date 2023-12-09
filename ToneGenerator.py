#Package Dependencies

import serial

import os

import time

from playaudio import playaudio as pa

import serial.tools.list_ports

 

#Functions

def readserial(port, audio, output):

    path = root + output

    readfile = open(path, 'a')

    ser = serial.Serial(port, 9600, timeout=0.1)

    while True:

        data = ser.readline().decode().strip()

        if data:

            data = int(data)

            response = ''

            if 0<=data<=255:

                response = "Best"

            if 256<=data<=512:

                response = "Good"

            if 513<=data<=768:

                response = "Bad"

            if 769<=data<=1023:

                response = "Worst"

            readfile.write(audio + " " + response + "\n")

            print(response)

            print(data)

            serial.Serial.reset_input_buffer(ser)

            break

    readfile.close()

#readserial('/dev/cu.usbmodem14401', '/Desktop/output.txt')

 

def playsound(wavfile):

    pa(root+wavfile)

 

def detectArduino():

    ports = list(serial.tools.list_ports.comports())

    error = False

    arduino_port = ''

    for p in ports:

        print(p)

        if "Arduino" in p.description:

            p.description.split(' ')

            arduino_port = p[0]

            print("Arduino detected...")

            return arduino_port

    error=True

    if error:

        raise Exception("No Arduino Port found, please enter manually.")

 

# Primary Code

root = os.path.expanduser('~')

go = True
print("Your root path is: ", root)
portname = ''

try:

    portname = detectArduino()

except:

    portname = input("Input the name of port connected to Arduino, typically starting with '/dev': ")

datafile = ''

soundfile = ''

dialtone = input("Input the file path for the dial tone: ")

while go == True:

    datafile = input("Input the path of file to output data to (or blank for same as previous): ") or datafile

    soundfile = input("Input the path of file containing sound information: ") or soundfile

    playsound(soundfile)
    print("Sound played")

    time.sleep(2)

    playsound(dialtone)
    print("Dial tone played")
    time.sleep(1)
   
    readserial(portname, soundfile, datafile)
   
   
    end_test = str(input("Press q to quit (or other keys to continue): "))

    end_test=end_test.lower()

    if end_test == 'q':

        go = False
