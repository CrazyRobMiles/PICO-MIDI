#Example 5: Control Vibrato

import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
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
            midi.send(NoteOn(self.midi_note, 100))
        if self.debouncer.rose:
            midi.send(NoteOff(self.midi_note, 100))
            
note_descriptions = [(board.GP6,60),(board.GP7,62),(board.GP10,64),
         (board.GP11,65),(board.GP16,67),(board.GP17,69),
         (board.GP18,71),(board.GP19,72)]

keyboard = []

for note in note_descriptions:
    (pin,midi_note)=note
    keyboard.append(Key(pin,midi_note))

# MIDI Control Change (CC) Numbers for Effects & Sound Control

# General Controls
CC_MODULATION = 1       # Modulation (often used for vibrato)
CC_VOLUME = 7           # Master volume
CC_PAN = 10             # Stereo panning (0=Left, 127=Right)
CC_EXPRESSION = 11      # Expression (secondary volume control)

# Sustain and Portamento
CC_SUSTAIN_PEDAL = 64   # Sustain pedal (Hold notes)
CC_PORTAMENTO = 65      # Portamento toggle (Glide between notes)

# Envelope & Filter
CC_SOUND_ATTACK = 73    # Attack time (faster attack = snappier)
CC_SOUND_RELEASE = 72   # Release time (longer = more sustain)
CC_SOUND_BRIGHTNESS = 74  # Low-pass filter cutoff (higher = brighter)
CC_SOUND_RESONANCE = 71  # Resonance (boosts filter peaks)

# Effects Controls
CC_REVERB = 91         # Reverb Send Level
CC_CHORUS = 93         # Chorus Send Level
CC_PHASER = 94         # Phaser Send Level (if supported)

midi.send(ControlChange(CC_MODULATION, 127))

while True:
    for key in keyboard:
        key.update()
    
