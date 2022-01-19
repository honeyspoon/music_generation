import random
import os
import time
import rtmidi
import signal
import sys

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
    notes = [[rtmidi.NOTE_OFF, i, 0] for i in range(128)]
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

    bpm = 120

    beat = 1
    measure = 4 * beat
    time_signature = 3

    key = 60
    scale = theory.major_scale(key)

    while True:
        progression = [
            1,
            4,
            5,
            5,
        ]

        chords = [ theory.diatonic_major_chord(key, i) for i in progression ]

        tracks = [
            [
                *play.space(chords, 1, 100),
            ],
        ]

        tracks = [sorted(track, key=lambda e: e[1]) for track in tracks]

        # w,_ = os.get_terminal_size()
        # for track in tracks:
        #     m = track[-1][1]
        #     print(m, w)
        #     for notes, ti in track:
        #         n = [c[1] for c in notes]
        #         t = '|start ' + ' '.join(map(theory.note_to_letter, n)) + ' ' if notes[0][0] == NOTE_ON else 'stop|' index = int((ti/m) * ( w - 4 ))
        #         print('|', ' ' * (index - 1), str(t).ljust(w - 4 - index , '-'), '|')

        # play.play_midi_events(midiout, tracks, bpm)

        def midi_stream():
            while True:
                y = [
                    [
                        *play.on([60, 64, 67], 100),
                        *play.on([60 - 12, 64 - 12, 67 - 12], 100),
                    ],
                    [
                        *play.off([60, 64, 67]),
                        *play.off([60 - 24, 64 - 24, 67 - 24]),
                    ]
                ]
                for e in y:
                    yield e

        play.play_midi_stream(midiout, midi_stream, bpm)

with midiout:
    c()
