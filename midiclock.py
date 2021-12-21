"""Receive MIDI clock and print out current BPM.

MIDI clock (status 0xF8) is sent 24 times per quarter note by clock generators.

"""

import argparse
import time
import threading
from collections import deque

from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

import theory

from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START, SONG_STOP)
import rtmidi
from rtmidi.midiutil import open_midiinput


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

def clear():
    unplay([i for i in range(128)])

def unplay(chord_notes):
    notes_off = [[NOTE_OFF, i, 0] for i in chord_notes]
    for off in notes_off:
        midiout.send_message(off)

def play(chord_notes, v=100):
    notes = [[NOTE_ON, i, v] for i in chord_notes]
    for note in notes:
        midiout.send_message(note)

bpm = 120.0
sync = False
running = True
samples = deque(maxlen=24)
last_clock = None
threads = []

def on_start():
    global running
    print('start', running)
    # scale = list(theory.major_scale(60))
    scale = list(theory.harmonic_minor_scale(60))
    print("scale", theory.note_to_letter(scale[0]))
    while running:
        duration = 120 / bpm
        chord = theory.random_chord(scale)
        print(chord, duration)
        play(chord)
        time.sleep(2 * duration)
        unplay(chord)

    print('clearing')
    clear()

def on_stop():
    print('stop')

def cb(event, _):
    global last_clock, bpm, sync, running, samples

    msg, _ = event

    if msg[0] == TIMING_CLOCK:
        now = time.time()

        if last_clock is not None:
            samples.append(now - last_clock)

        last_clock = now

        if len(samples) >= 2:
            bpm = 2.5 / (sum(samples) / len(samples))
            sync = True

    elif msg[0] in (SONG_CONTINUE, SONG_START):
        running = True
        thread = threading.Thread(target=on_start)
        thread.start()
    elif msg[0] == SONG_STOP:
        running = False
        on_stop()

def main():
    try:
        m_in, _ = open_midiinput(use_virtual=True)
    except (EOFError, KeyboardInterrupt):
        return 1

    m_in.set_callback(cb)
    m_in.ignore_types(timing=False)

    try:
        print("Waiting for clock sync...")
        # while True:
        #     if clock.running:
        #         if clock.sync:
        #             pass
        #             # print("%.2f bpm" % clock.bpm, duration)
        #             # play([60], 1)
        #         else:
        #             print("%.2f bpm (no sync)" % clock.bpm)
        while True:
            pass

    except KeyboardInterrupt:
        pass
    finally:
        m_in.close_port()
        del m_in


if __name__ == '__main__':
    main()
