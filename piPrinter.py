###########################################
# First test of 7 segment display
# on RPi Pico. Digits of Pi
#
# Author: Aleks Krachanko
#
# Description: This is a small piece of 
# code that uses a Raspberry Pi Pico
# to print the digits of pi to a 7 
# segment display. The pi_digits 
# variable sets to what precision this 
# is done (number of digits after decimal)
###########################################

from machine import Pin
import time 

pi_digits = 1000 # the precision of pi you'd like
ellipsis_length = 10 # length of ellipsis before starting from first digit again

seg_pins = [0,1,2,3,4,5,6,7] # GPIO pins where 7 segment is connected (set accordingly)

segments = [Pin(seg_pins[0],Pin.OUT),  # sets up segments array for 7 segment display
            Pin(seg_pins[1],Pin.OUT),
            Pin(seg_pins[2],Pin.OUT),
            Pin(seg_pins[3],Pin.OUT),
            Pin(seg_pins[4],Pin.OUT),
            Pin(seg_pins[5],Pin.OUT),
            Pin(seg_pins[6],Pin.OUT),
            Pin(seg_pins[7],Pin.OUT)]


delay_t = 0.4 # time delay between digits
gap_t = 0.1 # time delay between digits

digitBitmap = { 0:0b11101110 , # bit array with how to create each digit
                1:0b00101000 ,
                2:0b11001101 ,
                3:0b01101101 ,
                4:0b00101011 ,
                5:0b01100111 ,
                6:0b11100111 ,
                7:0b00101100 ,
                8:0b11101111 ,
                9:0b01101111 }

masks = { 'a': 0b00000100, # bit array with each segments position
          'b': 0b00001000,
          'c': 0b00100000,
          'd': 0b01000000,
          'e': 0b10000000,
          'f': 0b00000010,
          'g': 0b00000001,
          'dp': 0b00010000 }

pins = { 'a': 5, # bit array with each masks GPIO pin number
         'b': 4,
         'c': 2,
         'd': 1,
         'e': 0,
         'f': 6,
         'g': 7,
         'dp': 3}

###################################################
# functions defined in this section are only called
# by the main code section

def renderChar(c): # function to set 7 segment display to given character
    clear_segments() 
    if c == '.': # catches the decimal point 
        segments[pins['dp']].high()
        return
    
    val = digitBitmap[c]
    
    for k,v in masks.items(): # sets all required segments to on
        if val&v == v:
            segments[pins[k]].high()


def clear_segments():  # function clears the 7seg display
    for seg in segments:
        seg.low()


def calcPi(limit):  # generator function for pi
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3  
                                         
    decimal = limit
    counter = 0

    while counter != decimal + 1:
            if 4 * q + r - t < n * t:
                    yield n
                    if counter == 0:
                            yield '.'
                    if decimal == counter:
                            print('')
                            break
                    counter += 1
                    nr = 10 * (r - n * t)
                    n = ((10 * (3 * q + r)) // t) - 10 * n
                    q *= 10
                    r = nr
            else:
                    nr = (2 * q + r) * l
                    nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
                    q *= k
                    t *= l
                    l += 2
                    k += 1
                    n = nn
                    r = nr
                    
###################################################

# main code loop 
while True:
    clear_segments() #starts with a "clean slate" on 7seg
    
    pi = calcPi(pi_digits) # calls pi generator function and saves to pi
    
    for d in pi: # loop through each digit of pi
        renderChar(d) 
        time.sleep(delay_t) 
        clear_segments() 
        time.sleep(gap_t) 
    
    i = 0
    while i < 10: # adds an ellipsis before starting at beginning again (10 periods).
        renderChar('.')
        time.sleep(delay_t)
        clear_segments()
        time.sleep(gap_t) 
        i += 1
