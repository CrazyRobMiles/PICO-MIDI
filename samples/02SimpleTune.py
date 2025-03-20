# Example 2: play a tune

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
# midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

beat_length = 0.5

# Twinkle Twinkle melody (MIDI note, duration in beats)
twinkle_melody = [
    (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),
    (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2)
]

for step in twinkle_melody:
    (note,delay)=step
    midi.send(NoteOn(note, 100))
    time.sleep(beat_length*delay)
    midi.send(NoteOff(note, 100))
