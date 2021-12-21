import time
import rtmidi
import rtmidi

import signal
import sys

import theory
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

def all_notes_off():
    notes = [[NOTE_OFF, i, 0] for i in range(128)]
    for note in notes:
        midiout.send_message(note)
    del midiout

def signal_handler(sig, frame):
    print('cleanup')
    all_notes_off()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def play(chord_notes, duration, duration_2, n=1, v=100):
    for _ in range(n):
        notes = [[NOTE_ON, i, v] for i in chord_notes]
        notes_off = [[NOTE_OFF, i, 0] for i in chord_notes]
        for note in notes:
            midiout.send_message(note)
        time.sleep(duration)
        for off in notes_off:
            midiout.send_message(off)
        time.sleep(duration_2)

def play_all(notes, duration, duration_2):
    for note in notes:
        play([note], duration, duration_2)

def a():
    while True:
        start = 60
        scale = theory.major_scale(start)
        play_all(scale, 0.5, 0.5)

def b():
    while True:
        print('=======')
        delay = 2 * 0.5
        delay_2 = 0
        base = 63

        # scale_1 = list(major_scale(base))
        scale_1 = list(theory.melodic_minor_scale(base))
        # scale_2 = list(theory.melodic_minor_scale(base + 5))
        # scale_2 = list(major_scale(base + 5))

        play(theory.random_chord(scale_1), delay, delay_2)
        play(theory.random_chord(scale_1), delay, delay_2)
        play(theory.random_chord(scale_1), delay, delay_2)

        # play(random_chord(scale_2), delay / 2, delay_2)
        # play(random_chord(scale_2), delay / 2, delay_2)

def c():
    pass

with midiout:
    # a()
    # b()
    c()
