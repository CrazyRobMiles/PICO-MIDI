#Example 4: Complete keyboard

version="Version 1.0"

import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.control_change import ControlChange

import busio as io
import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer
import adafruit_ssd1306
import rotaryio
import neopixel

class Col:
    
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (10, 10, 10)
    VIOLET = (127,0,155)
    INDIGO = (75,0,130)
    ORANGE = (255,165,0)

    values=(RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, GREY, WHITE)
     
    @staticmethod
    def dim(col):
        return (col[0]/40, col[1]/40, col[2]/40)
    
MUSIC_STATE = 0
DRUMS_STATE = 1

NO_OF_STATES = 2

state_number = 0

class Key():
    def __init__(self, pin, midi_note, drum_note,pixel):
        self.pin = pin
        tmp_pin = DigitalInOut(pin)
        tmp_pin.pull = Pull.UP
        self.debouncer = Debouncer(tmp_pin,interval=0.01)
        self.midi_note = midi_note
        self.drum_note = drum_note
        self.pixel = pixel
        self.note_playing = False
        
    def play_note(self):
        midi.send(NoteOn(self.midi_note, 100))
        self.note_playing = True
        pixels[self.pixel]=Col.RED
        
    def clear_note(self):
        if self.note_playing:
            midi.send(NoteOff(self.midi_note, 100))
            self.note_playing = False
        pixels[self.pixel]=Col.GREY
        
    def clear_drum(self):
        pixels[self.pixel]=Col.BLUE
        
    def play_drum(self):
        midi.send(NoteOn(self.drum_note, 100),channel=9)
        pixels[self.pixel]=Col.CYAN
        
    def clear(self):
        if state_number == 0:
            self.clear_note()
        elif state_number == 1:
            self.clear_drum()
        
    def play(self):
        if state_number == 0:
            self.play_note()
        elif state_number == 1:
            self.play_drum()
        
    def update(self):
        self.debouncer.update()
        
        if self.debouncer.fell:
            self.play()
                
        if self.debouncer.rose:
            self.clear()
            
class Display():
    
    WIDTH=128
    HEIGHT=32

    def __init__(self,sda,scl,orientation=1):
        print("Display starting")
        self.i2c = io.I2C(sda, scl)
        self.oled = adafruit_ssd1306.SSD1306_I2C(Display.WIDTH, Display.HEIGHT, self.i2c)
        if orientation==1:
            self.oled.rotation = 2
        else:
            self.oled.rotation = 0
        self.topline=""
        self.midline=""
        self.baseline=""
        self.old_topline=""
        self.old_midline=""
        self.old_baseline=""
        self.oled.fill(0)

    def place_text(self,text,y,size):
        x = int((Display.WIDTH-(len(text)*6*size))/2)
        self.oled.text(text,x,y,1,size=size)
        
    def render(self):
        oled = self.oled
        oled.fill(0)
        self.place_text(self.topline,0,1)
        self.place_text(self.midline,9,1)
        self.place_text(self.baseline,25,1)
        self.oled.show()
        
    def update(self):
        if self.topline==self.old_topline and self.midline==self.old_midline and self.baseline==self.old_baseline:
            return
        self.render()
        self.old_topline = self.topline
        self.old_midline = self.midline
        self.old_baseline = self.baseline
        
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

class VoiceSetting:
    
    def __init__(self):
        self.name = "Voice"
        self.set(0)
        
    def update(self,change):
        
        if change==0:
            return
        
        new_voice = self.voice + change
        
        if new_voice<0:
            new_voice=0
        
        if new_voice > len(midi_instruments):
            new_voice = len(midi_instruments)
            
        if new_voice == self.voice:
            return
        
        self.set(new_voice)
        
    def set(self,voice):
        if voice<0 or voice>=len(midi_instruments):
            return
        
        self.voice = voice
        (voice_name,number)=midi_instruments[voice]
        midi.send(ProgramChange(number))
        
    def show(self):
        display.topline=self.name
        (voice_name,number)=midi_instruments[self.voice]
        display.midline=voice_name

class ControlSetting:
    
    def __init__(self,name, message_number,initial_value=0):
        self.name = name
        self.message_number = message_number
        self.set(initial_value)
        
    def update(self,change):
        
        if change==0:
            return
        
        new_level = self.level + change
        
        if new_level<0:
            new_level=0
        
        if new_level > 127:
            new_voice = 127
            
        if new_level == self.level:
            return
        
        self.set(new_level)
        

    def set(self,level):
        if level<0 or level>127:
            return
        self.level=level
        midi.send(ControlChange(self.message_number, level))
        
    def show(self):
        display.topline=self.name
        display.midline=str(self.level)

class MusicBox():
    
    def __init__(self,
                 notes,
                 midi_tx, midi_rx,
                 encoder_a,encoder_b,encoder_button,
                 display_sda,display_scl,
                 pixel_pin, orientation=0):
        global midi
        global display
        global pixels
        pixels_per_note=3
        pixel = 1
        voice=0
        # Create keys
        keyboard = []
        for note in notes:
            (pin,midi_note,drum_note)=note
            keyboard.append(Key(pin,midi_note,drum_note,pixel))
            pixel=pixel=pixel+pixels_per_note

        self.keyboard = keyboard
        # Make encoder
        self.encoder= rotaryio.IncrementalEncoder(encoder_a, encoder_b)
        self.old_encoder_pos = self.encoder.position
        # Make encoder button
        tmp_pin = DigitalInOut(encoder_button)
        tmp_pin.pull = Pull.UP
        self.encoder_button = Debouncer(tmp_pin,interval=0.01)
        self.encoder_pressed = False
        display = Display(display_sda,display_scl,orientation)
        display.topline="Music Box"
        display.midline="Rob Miles"
        display.baseline=version
        display.update()
        time.sleep(1)
        pixels_per_note = 3
        pixel_length = len(notes)*pixels_per_note
        pixels = neopixel.NeoPixel(pixel_pin,pixel_length,auto_write=False)
        
        for key in keyboard:
            pixels[key.pixel] = Col.GREY

        pixels.show()

        if midi_tx != None:
            uart = io.UART(board.GP12, board.GP13, baudrate=31250)
            midi = adafruit_midi.MIDI(midi_out=uart, out_channel=0)
        else:
            midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
            
        self.settings = [ VoiceSetting(), ControlSetting("Reverb",91), ControlSetting("Chorus",93), ControlSetting("Vibrato",1), ControlSetting("Portmanto",5) ]
        self.select_setting(0)
        
    def next_setting(self):
        new_setting = self.setting_number + 1
        if new_setting >= len(self.settings):
            new_setting=0
        self.select_setting(new_setting)
            
    def select_setting(self,number):
        if number<0 or number>=len(self.settings):
            return
        
        self.setting_number = number
        setting = self.settings[number]
        setting.show()
        
    def encoder_update(self):
        global state_number
        self.encoder_button.update()
        if self.encoder_button.fell:
            self.next_setting()
            self.encoder_down_time = time.monotonic()
            self.encoder_pressed=True
        if self.encoder_button.rose:
            self.encoder_pressed=False
        
        if self.encoder_pressed:
            
            current_time = time.monotonic()
            
            if current_time-self.encoder_down_time > 2.0:

                state_number = state_number + 1
                
                if state_number >= NO_OF_STATES:
                    state_number = 0
                    
                for key in self.keyboard:
                    key.clear()
                    
                self.encoder_down_time = current_time
        
        new_encoder_pos = self.encoder.position
        
        if new_encoder_pos == self.old_encoder_pos:
            return

        change = self.old_encoder_pos-new_encoder_pos
        
        self.old_encoder_pos=new_encoder_pos
        setting = self.settings[self.setting_number]
        setting.update(change)
        setting.show()
        
    def update(self):
        for key in self.keyboard:
            key.update()
        self.encoder_update()
        display.update()
        pixels.show()
    
ACOUSTIC_BASS_DRUM = 35
ACOUSTIC_SNARE = 38
CLOSED_HIHAT = 42
OPEN_HIHAT = 46
CRASH_CYMBAL_1 = 49
RIDE_CYMBAL_1 = 51
LOW_TOM = 45
LOW_FLOOR_TOM = 41

notes = [(board.GP6,60,ACOUSTIC_BASS_DRUM),
         (board.GP7,62,ACOUSTIC_SNARE),
         (board.GP10,64,CLOSED_HIHAT),
         (board.GP11,65,OPEN_HIHAT),
         (board.GP16,67,CRASH_CYMBAL_1),
         (board.GP17,69,RIDE_CYMBAL_1),
         (board.GP18,71,LOW_TOM),
         (board.GP19,72,LOW_FLOOR_TOM)]

box = MusicBox(notes,
               board.GP12, board.GP13, #midi
               board.GP21,board.GP20,board.GP22, # rotary
               board.GP5, board.GP4, #display
               board.GP0) #pixel

while True:
    box.update()

    


