#Example 7: Drum kit

import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import busio as io
import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer

## Drive synth from the serial port
## comment out these lines for usb use
uart = io.UART(board.GP12, board.GP13, baudrate=31250)
midi = adafruit_midi.MIDI(midi_out=uart, out_channel=0)

## Drive a synth from the USB port
## comment out this line for serial use
# midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Drum sound mapping

ACOUSTIC_BASS_DRUM = 35
ACOUSTIC_SNARE = 38
CLOSED_HIHAT = 42
OPEN_HIHAT = 46
CRASH_CYMBAL_1 = 49
RIDE_CYMBAL_1 = 51
LOW_TOM = 45
LOW_FLOOR_TOM = 41

class Key():
    def __init__(self, pin, midi_note):
        self.pin = pin
        tmp_pin = DigitalInOut(pin)
        tmp_pin.pull = Pull.UP
        self.debouncer = Debouncer(tmp_pin,interval=0.01)
        self.midi_note = midi_note
        
    def update(self):
        self.debouncer.update()
        if self.debouncer.fell:
            midi.send(NoteOn(self.midi_note, 100),channel=9)

midi.send(NoteOn(ACOUSTIC_BASS_DRUM, 100),channel=9)         
            
note_descriptions = [(board.GP6,ACOUSTIC_BASS_DRUM),
                     (board.GP7,ACOUSTIC_SNARE),
                     (board.GP10,CLOSED_HIHAT),
                     (board.GP11,OPEN_HIHAT),
                     (board.GP16,CRASH_CYMBAL_1),
                     (board.GP17,RIDE_CYMBAL_1),
                     (board.GP18,LOW_TOM),
                     (board.GP19,LOW_FLOOR_TOM)]

keyboard = []

for note in note_descriptions:
    (pin,midi_note)=note
    keyboard.append(Key(pin,midi_note))

while True:
    for key in keyboard:
        key.update()

    



