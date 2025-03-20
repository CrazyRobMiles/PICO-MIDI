# Example 3: Play a note when a key is pressed

import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import busio as io
import board

uart = io.UART(board.GP12, board.GP13, baudrate=31250)
midi = adafruit_midi.MIDI(midi_out=uart, out_channel=0)

from digitalio import DigitalInOut, Pull
note1_pin = DigitalInOut(board.GP6)
note1_pin.pull = Pull.UP

from adafruit_debouncer import Debouncer
note1_debounce = Debouncer(note1_pin,interval=0.01)

while(True):
    note1_debounce.update()
    if note1_debounce.fell:
         midi.send(NoteOn(60, 100))
    if note1_debounce.rose:
         midi.send(NoteOff(60, 100))

