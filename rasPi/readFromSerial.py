#!/usr/bin/python

# A simple script to read incoming data from a usb port
# and print it to the console
import pytz # sudo easy_install --upgrade pytz
import serial, time, requests, json
from datetime import datetime
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

#Assign a URL variable for cleanliness
url = 'http://ec2-54-202-217-172.us-west-2.compute.amazonaws.com/api/v1/readings'

ser = serial.Serial()
# This port will be different of different machines check correct port with
# $ python -m serial.tools.list_ports
#ser.port = "/dev/cu.usbserial-DN01Q8E0" #For mini-USB cable
# ser.port = "/dev/cu.usbserial-A5058SOW" #For FTDI cable
ser.port = "/dev/ttyUSB0" #For raspi mini-usb cable
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
# ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
#Try to open the port
try: 
    print("Opening serial port and waiting for data")
    ser.open()
except IOError, e:
    print "error open serial port: " + str(e)
    #Send message to the Cloud
    
    # r = requests.post(url,
    # headers = {'Content-type': 'application/json'}, #Should this be Error-type or Content-type? Where do I post the errors?
    # data = {'error': e})
    #execfile("launcher.sh")
    exit()

if ser.isOpen():
    while True: #We caught an error. We assume it won't happen next time so just naively try the same code again
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output and discard all that is in buffer
            time.sleep(0.5)  #give the serial port sometime to receive the data
            while True:
                response = ser.readline() #TODO: Got a timeout here
                                                # ^CTraceback (most recent call last):
                                                #   File "rasPi/readFromSerial.py", line 51, in <module>
                                                #     response = ser.readline()
                                                #   File "/Library/Python/2.7/site-packages/serial/serialposix.py", line 472, in read
                                                #     ready, _, _ = select.select([self.fd, self.pipe_abort_read_r], [], [], timeout.time_left())
                #Only print responses with an actual message in them
                if response != "":
                    #TODO: Strip \n from response
                    dateString = '%Y/%m/%d %H:%M:%S'
                    dateString = str(datetime.now(pytz.timezone('US/Pacific')))
                    response = response.rstrip()
                    response += " \"timeStamp\"  : \"" + dateString + "\"}"
                    j = json.loads(response)
                    # r = requests.post('http://ec2-54-202-217-172.us-west-2.compute.amazonaws.com/api/v1/readings',
                    #     headers = {'Content-type': 'application/json'}, 
                    #     data = json.dumps(j))
                    r = requests.post('http://localhost:3000/api/v1/readings',
                        # headers = {'Content-type': 'application/json', 'Authorization' : 'rasPiAuth..-246'}, 
                        headers={'Authorization' : 'rasPiAuth..0246', 'Content-type': 'application/json'},
                        data = json.dumps(j))
                    print ""
                    print "******"
                    print j
                    print "**********"
                    print json.dumps(j)
                    print r
                    print r.content

        except Exception, e1:
            print "We caught an error! : " + str(e1)
            r = requests.post(url,
            headers = {'Content-type': 'application/json'}, #Should this be Error-type or Content-type? Where do I post the errors?
            data = {'error': e1})
            continue #Go to the start of the loop and try again

else:
    print "cannot open serial port "
    #Need to post this error too?

ser.close()



