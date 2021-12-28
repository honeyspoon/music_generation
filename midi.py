import random
import os
import time
import rtmidi
import rtmidi

import signal
import sys
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

import theory
import play

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

def all_notes_off():
    global midiout
    notes = [[NOTE_OFF, i, 0] for i in range(128)]
    for note in notes:
        midiout.send_message(note)
    del midiout

def signal_handler(sig, frame):
    print('cleanup')
    all_notes_off()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def c():
    time.sleep(0.5)
    baseline = []

    base = 60
    melody = [
        ([60], 8),
        ([62], 8),
        ([64], 4),
    ]

    tracks = [
        *baseline,
        *melody
    ]

    bpm = 120

    base = 65
    scale = theory.major_scale(base)

    while True:
        # progression = [
        #     (1, theory.major_chord),
        #     (5, theory.major_chord),
        #     (6, theory.minor_chord),
        #     (4, theory.major_chord)
        # ]

        progression = [
            (2, theory.minor_seventh_chord),
            (5, theory.major_seventh_chord),
            (1, theory.major_seventh_chord),
        ]

        # progression = [
        #     (1, theory.major_chord),
        #     (1, theory.major_chord),
        #     (1, theory.major_chord),
        #     (1, theory.major_chord),
        #
        #     (4, theory.major_chord),
        #     (4, theory.major_chord),
        #     (1, theory.major_chord),
        #     (1, theory.major_chord),
        #
        #     (5, theory.major_chord),
        #     (4, theory.major_chord),
        #     (1, theory.major_chord),
        #     (1, theory.major_chord),
        # ]

        # progression = [
        #     (1, theory.major_chord),
        #     (6, theory.minor_chord),
        #     (4, theory.major_chord),
        #     (5, theory.major_chord),
        # ]

        # progression = [
        #     (random.randint(1, 7), random.choice(theory.chords)) for _ in range(16)
        # ]

        # progression = [
        #     (1, theory.major_chord),
        #     (5, theory.major_chord),
        #     (6, theory.minor_chord),
        #     (3, theory.minor_chord),
        #
        #     (4, theory.major_chord),
        #     (1, theory.major_chord),
        #     (4, theory.major_chord),
        #     (5, theory.major_chord),
        # ]
        #

        chords = [f(scale[i - 1]) for i, f in progression]
        chords_2 = [f(scale[i - 1] - 24 - 7) for i, f in progression]


        tracks = [
            [
                *play.space(chords, 1, 100),
            ],
            # [
            #     *space(chords_2, 2, 100),
            # ]
        ]

        tracks = [sorted(track, key=lambda e: e[1]) for track in tracks]

        # w,_ = os.get_terminal_size()
        # for track in tracks:
        #     m = track[-1][1]
        #     print(m, w)
        #     for notes, ti in track:
        #         n = [c[1] for c in notes]
        #         t = '|start ' + ' '.join(map(theory.note_to_letter, n)) + ' ' if notes[0][0] == NOTE_ON else 'stop|'
        #         index = int((ti/m) * ( w - 4 ))
        #         print('|', ' ' * (index - 1), str(t).ljust(w - 4 - index , '-'), '|')

        play.play_midi_events(midiout, tracks, bpm)


with midiout:
    c()
