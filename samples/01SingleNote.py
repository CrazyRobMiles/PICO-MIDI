# Example 1: play a single note

import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import busio as io
import board

## Drive synth from the serial port
## comment out these lines for usb use
uart = io.UART(board.GP12, board.GP13, baudrate=31250)
midi = adafruit_midi.MIDI(midi_out=uart, out_channel=0)

## Drive a synth from the USB port
## comment out this line for serial use
## midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

midi.send(NoteOn(60, 100))
time.sleep(0.5)
midi.send(NoteOff(60, 100))
