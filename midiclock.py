import sys
import math
import collections
import os
import signal
import play
import time

import thread_ex
import multiprocessing
from collections import deque

from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

import theory

from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START, SONG_STOP)
import rtmidi
from rtmidi.midiutil import open_midiinput

def signal_handler(sig, frame):
    print('cleanup')
    clear()
    # m_in.close_port()
    # del m_in
    sys.exit(0)

def clear():
    global event_q
    notes_off = [[NOTE_OFF, i, 0] for i in range(128)]
    for off in notes_off:
        event_q.put(off)

#     unplay([i for i in range(128)])

# def unplay(chord_notes):
#     notes_off = [[NOTE_OFF, i, 0] for i in chord_notes]
#     for off in notes_off:
#         midiout.send_message(off)
#
# def play(chord_notes, v=100):
#     notes = [[NOTE_ON, i, v] for i in chord_notes]
#     for note in notes:
#         midiout.send_message(note)

bpm = 120.0
sync = False
running = True
samples = deque(maxlen=24)
last_clock = None
# threads = []
procs = []
event_q = multiprocessing.Queue()

def print_tracks(tracks):
    w,_ = os.get_terminal_size()
    for track in tracks:
        notes_dict = collections.defaultdict(list)
        for notes, start_time in track:
            a = '-'.join(map(lambda e: theory.note_to_letter(e[1]), notes))
            notes_dict[a].append(start_time)

        m = 0
        mn = 0
        for k, v in notes_dict.items():
            mn = max(mn, len(k))
            m = max(m, *v)


        def lerp(a, b, c):
            # return math.floor((a / b) * c)
            return int((a / b) * c)

        w2 = w - 1 - mn - 1
        print(''.ljust(mn), '|', sep='',end='')
        for i in range(1,int(m / 4)):
            print(' ' * lerp(4,m, w2), '|', sep='', end='')

        print()
        for k, v in notes_dict.items():
            i = iter(v)
            pairs = []
            for start in i:
                stop = next(i)
                pairs.append((start, stop))

            print(k.ljust(mn), '|', sep='',end='')
            for start, stop in pairs:

                start_i = lerp(start, m, w2)
                stop_i = lerp(stop, m, w2)

                print(
                    # (start, start_i, stop, stop_i, m, w2),
                    ' ' * (start_i), '[', '-'*(stop_i - start_i - 1), ']', sep='', end='')
            print()


    print()

def on_start(event_q):
    print(time.time(), 'start')
    base = 65
    while True:
        scale = theory.major_scale(base)
        progression = [
            (1, theory.minor_seventh_chord),
            (4, theory.minor_seventh_chord),
            (5, theory.minor_seventh_chord),
            (1, theory.minor_seventh_chord),
        ]

        chords = [f(scale[i - 1]) for i, f in progression]

        scale = theory.major_scale(base + 7)

        chords_2 = [f(scale[i - 1]) for i, f in progression]

        tracks = [
            [
                *play.space(chords, 1, 100),
                *play.space(chords_2, 1, 100, start=16),
            ],
            # [
            #     *play.space(chords_2, 2, 100),
            # ]
        ]

        tracks = [sorted(track, key=lambda e: e[1]) for track in tracks]

        print_tracks(tracks)
        play.play_midi_events(tracks, bpm, event_q)

def on_stop():
    print(time.time(), 'stop')
    clear()

def send_events(q):
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    while True:
        event = q.get()

        if event[0] != 128:
            print('new event', event)
        midiout.send_message(event)
        # play.play_midi_events(midiout)


def kill_procs(procs):
    print('killing procs', procs)
    for p in procs:
        p.terminate()

def cb(event, _):
    global last_clock, bpm, sync, running, samples, procs, event_q

    msg, _ = event

    multiprocessing.Process(target = send_events, args = (event_q,)).start()

    if msg[0] == TIMING_CLOCK:
        now = time.time()

        if last_clock is not None:
            samples.append(now - last_clock)

        last_clock = now

        if len(samples) >= 2:
            bpm = 2.5 / (sum(samples) / len(samples))
            sync = True

    elif msg[0] in (SONG_CONTINUE, SONG_START):
        kill_procs(procs)
        running = True
        p = thread_ex.thread_with_exception(on_start)

        p = multiprocessing.Process(target=on_start, args=(event_q, ))

        p.start()
        procs.append(p)
    elif msg[0] == SONG_STOP:
        running = False
        kill_procs(procs)
        on_stop()

def main():
    try:
        m_in, _ = open_midiinput(use_virtual=True)
    except (EOFError, KeyboardInterrupt):
        return 1

    m_in.set_callback(cb)
    m_in.ignore_types(timing=False)

    signal.signal(signal.SIGINT, signal_handler)

    print("Waiting for clock sync...")
    while True:
        pass

if __name__ == '__main__':
    main()
