# https://github.com/jakka351/TPMS-ABS
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import can
import time
import os
import queue
from threading import Thread
import sys, traceback
''' This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This is distributed in the hope 
 that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
 See the GNU General Public License for more details. You should have received a copy of the GNU General Public License
 along with this file.  If not, see <https://www.gnu.org/licenses/>. '''

c                      = ''
count                  = 0  
# CAN Id's
SAS                    = 0x90 
ABS                    = 0x4B0 

def scroll():
    print('''  
             
             ''')
        
def setup():
    global bus
    try:
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan_native')
    except OSError:
        sys.exit() # quits if there is no canbus interface
    print("                      ")
    print("        CANbus active on", bus)   
    print("        ...")     #this line gets replaced by the next matching can frame
    print("        ...")             # this line gets replaced by the button in the car that is pushed
    
def msgbuffer():
    global message, q, SAS, ABS                                          
    while True:
        message = bus.recv()          # if recieving can frames then put these can arb id's into a queue
        if message.arbitration_id == SAS:                        
            q.put(message)
        elif message.arbitration_id == ABS:                        
            q.put(message)
        else:
            pass

def cleanline():                      # cleans the last output line from the console
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():                    # cleans the whole console screen
    os.system("clear")

def ccp():
    cleanline()
    cleanline()
    print(message)
                        
def main(): 
global bus, message, q, SAS, ABS            
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):                               # wait for messages to queue
                    pass
                message = q.get()   
                c = '{0:f},{1:d},'.format(message.timestamp,count)

                if message.arbitration_id in SAS:
                    message.data[0] = SteeringAnglePos
                    message.data[1] = SteeringAngleNeg

                
                elif message.arbitration_id in ABS:
                    if message.data[0:7] != 0x00:
                        message.data[0] = FrontLeftCoarse
                        message.data[1] = FrontLeftFine
                        message.data[2] = FrontRightCoarse
                        message.data[3] = FrontRightFine
                        message.data[4] = RearLeftCoarse
                        message.data[5] = RearLeftFine
                        message.data[6] = RearRightCoarse
                        message.data[7] = RearRightFine
                        
                        while SteeringAngleNeg == 0x00 and SteeringAnglePos == 0x00 #Or in almost 0 degrees range

                        if FrontRightCoarse == RearRightCoarse and FrontLeftCoarse == RearLeftCoarse and RearRightCoarse == RearLeftCoarse:
                            FrontLeftTyrePressure  = 1.000
                            FrontRightTyrePressure = 1.000
                            RearLeftTyrePressure   = 1.000
                            RearRightTyrePressure  = 1.000

                        elif FrontRightCoarse != RearRightCoarse or FrontRightCoarse != FrontLeftCoarse or FrontRightCoarse != RearLeftCoarse:
                            FrontRightTyrePressure = FrontRightCoarse - (RearRightCoarse - FrontRightCoarse)

                    elif message.data[0:7] == 0x00:
                            print("Vehicle Stationary, TPMS Inactive")
                            time.sleep(0.25)
                            pass
                                              
    except KeyboardInterrupt:
        sys.exit(0)                                              # quit if ctl + c is hit
    except Exception:
        traceback.print_exc(file=sys.stdout)                     # quit if there is a python problem
        sys.exit()
    except OSError:
        sys.exit()                                               # quit if there is a system issue

############################
# TPMS-ABS
############################

if __name__ == "__main__":
    q                      = queue.Queue()                       #
    rx                     = Thread(target = msgbuffer)          #
    cleanscreen()                                                # clean the console screen
    scroll()                                                     # scroll out fancy logo text
    setup()                                                      # set the can interface
    rx.start()                                                   # start the rx thread and queue msgs
    main()                                                       # match ca
