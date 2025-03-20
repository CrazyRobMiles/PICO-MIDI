#Example 5: Keyboard voices

import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.program_change import ProgramChange
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

midi_instruments = [
    ("Acoustic Grand Piano", 0),
    ("Bright Acoustic Piano", 1),
    ("Electric Grand Piano", 2),
    ("Honky-tonk Piano", 3),
    ("Electric Piano 1", 4),
    ("Electric Piano 2", 5),
    ("Harpsichord", 6),
    ("Clavinet", 7),
    ("Celesta", 8),
    ("Glockenspiel", 9),
    ("Music Box", 10),
    ("Vibraphone", 11),
    ("Marimba", 12),
    ("Xylophone", 13),
    ("Tubular Bells", 14),
    ("Dulcimer", 15),
    ("Drawbar Organ", 16),
    ("Percussive Organ", 17),
    ("Rock Organ", 18),
    ("Church Organ", 19),
    ("Reed Organ", 20),
    ("Accordion", 21),
    ("Harmonica", 22),
    ("Tango Accordion", 23),
    ("Acoustic Guitar (nylon)", 24),
    ("Acoustic Guitar (steel)", 25),
    ("Electric Guitar (jazz)", 26),
    ("Electric Guitar (clean)", 27),
    ("Electric Guitar (muted)", 28),
    ("Overdriven Guitar", 29),
    ("Distortion Guitar", 30),
    ("Guitar Harmonics", 31),
    ("Acoustic Bass", 32),
    ("Electric Bass (finger)", 33),
    ("Electric Bass (pick)", 34),
    ("Fretless Bass", 35),
    ("Slap Bass 1", 36),
    ("Slap Bass 2", 37),
    ("Synth Bass 1", 38),
    ("Synth Bass 2", 39),
    ("Violin", 40),
    ("Viola", 41),
    ("Cello", 42),
    ("Contrabass", 43),
    ("Tremolo Strings", 44),
    ("Pizzicato Strings", 45),
    ("Orchestral Harp", 46),
    ("Timpani", 47),
    ("String Ensemble 1", 48),
    ("String Ensemble 2", 49),
    ("Synth Strings 1", 50),
    ("Synth Strings 2", 51),
    ("Choir Aahs", 52),
    ("Voice Oohs", 53),
    ("Synth Choir", 54),
    ("Orchestra Hit", 55),
    ("Trumpet", 56),
    ("Trombone", 57),
    ("Tuba", 58),
    ("Muted Trumpet", 59),
    ("French Horn", 60),
    ("Brass Section", 61),
    ("Synth Brass 1", 62),
    ("Synth Brass 2", 63),
    ("Soprano Sax", 64),
    ("Alto Sax", 65),
    ("Tenor Sax", 66),
    ("Baritone Sax", 67),
    ("Oboe", 68),
    ("English Horn", 69),
    ("Bassoon", 70),
    ("Clarinet", 71),
    ("Piccolo", 72),
    ("Flute", 73),
    ("Recorder", 74),
    ("Pan Flute", 75),
    ("Blown Bottle", 76),
    ("Shakuhachi", 77),
    ("Whistle", 78),
    ("Ocarina", 79),
    ("Lead 1 (square)", 80),
    ("Lead 2 (sawtooth)", 81),
    ("Lead 3 (calliope)", 82),
    ("Lead 4 (chiff)", 83),
    ("Lead 5 (charang)", 84),
    ("Lead 6 (voice)", 85),
    ("Lead 7 (fifths)", 86),
    ("Lead 8 (bass+lead)", 87),
    ("Pad 1 (new age)", 88),
    ("Pad 2 (warm)", 89),
    ("Pad 3 (polysynth)", 90),
    ("Pad 4 (choir)", 91),
    ("Pad 5 (bowed)", 92),
    ("Pad 6 (metallic)", 93),
    ("Pad 7 (halo)", 94),
    ("Pad 8 (sweep)", 95),
    ("FX 1 (rain)", 96),
    ("FX 2 (soundtrack)", 97),
    ("FX 3 (crystal)", 98),
    ("FX 4 (atmosphere)", 99),
    ("FX 5 (brightness)", 100),
    ("FX 6 (goblins)", 101),
    ("FX 7 (echoes)", 102),
    ("FX 8 (sci-fi)", 103),
    ("Sitar", 104),
    ("Banjo", 105),
    ("Shamisen", 106),
    ("Koto", 107),
    ("Kalimba", 108),
    ("Bagpipe", 109),
    ("Fiddle", 110),
    ("Shanai", 111),
    ("Tinkle Bell", 112),
    ("Agogo", 113),
    ("Steel Drums", 114),
    ("Woodblock", 115),
    ("Taiko Drum", 116),
    ("Melodic Tom", 117),
    ("Synth Drum", 118),
    ("Reverse Cymbal", 119),
    ("Guitar Fret Noise", 120),
    ("Breath Noise", 121),
    ("Seashore", 122),
    ("Bird Tweet", 123),
    ("Telephone Ring", 124),
    ("Helicopter", 125),
    ("Applause", 126),
    ("Gunshot", 127),
]

def select_voice(number):
    if number<0 or number>len(midi_instruments):
        return
    
    (name,voice_number)=midi_instruments[number]
    midi.send(ProgramChange(voice_number))
    print(f"Voice {name} selected")

keyboard = []

for note in note_descriptions:
    (pin,midi_note)=note
    keyboard.append(Key(pin,midi_note))

select_voice(124)

while True:
    for key in keyboard:
        key.update()
