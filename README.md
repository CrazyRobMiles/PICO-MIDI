# PICO-MIDI
Some notes on getting started with MIDI on a PICO using a M5Stack devices [MIDI](https://docs.m5stack.com/en/unit/Unit-MIDI) and [Synth](https://docs.m5stack.com/en/unit/Unit-Synth)
 
![M5 Stack MIDI devices](/images/m5%20synth%20and%20midi.jpg)
These notes have been written for the Raspberry Pi PICO family. The code might need slight modification to run on other devices supporting Circuit Python.  

# PICO MusicBox

![PICO MusicBox device](images/PICO%20MusicBox.jpg) 
The PICO MusicBox is powered by Synth device and a PICO. It has an eight button keyboard, a rotary encoder for selecting options and a small OLED panel. It also has coloured leds for each note. You can find the case design in the case folder in this repository. Control software for the MusicBox is in the python folder. Copy all the library files, the font file and code.py onto your Circuit Python device to get it going. 

## Software Installation
The music box is powered by a Circuit Python program. Follow the instructions [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to install version 9 on your PICO. That's the one for which the pre-built image will work). Then plug your PICO into your computer. An external drive will open up. Copy the entire contents of the python folder onto the root of this drive. Now unplug your PICO and plug it back in again. The external drive will no longer appear on your computer and your PICO will be running the music software.

## MusicBox Commands

* Press any key to make a note, starting at middle C in the major scale
* Turn the encoder to select options
* Press the encoder in to select the option that you are currently adjusting
* Hold the encoder down for two seconds to switch between "drum" and "keyboard" modes. In drum mode the key lights are blue, in keyboard mode the key lights are grey.

# Sample Code

The samples folder contains small sample programs:

* **01SingleNote** - plays a single note
* **O2SimpleTune** - plays a simple tune
* **03SingleNote** - implements key behaviour for a single note
* **04Keyboard** - implements an eight key keyboard
* **05Voices** - shows how different voices are selected
* **06Control** - sends control messages to change the sound output
* **07Drums** - shows how drums are played 

# Hardware connections

## Minimal synth
![M5 Stack synth and PICO](/images/midi%20wiring.jpg)

You can make a minimal sound device  by connecting the PICO to one of the MIDI devices. The synth is powered from the VSYS 5-volt output from the PICO and connected to GPIO12 and GPIO13 for serial communication. If you use different pins you will have to modify the example code here.

## PICO MusicBox

![PICO keyboard circuit](/images/musicbox%20circuit.png)

This is the circuit for the complete music box. The code below maps the hardware below onto the software. If you use different connections you will need to change this.

```
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
```

# MIDI on CircuitPython
To send MIDI commands from a CircuitPython program we use the [AdaFruit MIDI library](https://docs.circuitpython.org/projects/midi/en/latest/api.html). The Python folder in this repository contains a lib folder which contains the required library files for Circuit Python version 9. Copy this folder onto your Circuit Python device. If you want to use a different version of Circuit Python on your device you can find the library bundles [here](https://docs.circuitpython.org/projects/bundle/en/latest/).

The resources you need are these:

* **adafruit_midi** folder for the MIDI class
* **adafruit_bus_device** folder for the serial port drivers 
* **Debouncer** for the input signal debouncer

Have Fun

Rob Miles