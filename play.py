
import time
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON
import time

def on(notes, v):
    return [[NOTE_ON, i, v] for i in notes]

def off(notes):
    return [[NOTE_OFF, i, 0] for i in notes]

def play_midi_stream(device, stream, bpm):
    beat_length = 120 / bpm

    for event in stream():
        print(event)
        for e in event:
            device.send_message(e)
        time.sleep(beat_length)

def play_midi_events(device, tracks, bpm):
    done = lambda: all(i is None for i in track_indexes)

    bar = 120 / bpm
    u = bar / 4

    t = 0
    track_indexes = [0] * len(tracks)

    while True:
        events = []
        for i, track in enumerate(tracks):
            if track_indexes[i] is None:
                continue
            while True:
                event, start_t = track[track_indexes[i]]

                if t != start_t:
                    # index -= 1
                    break

                for e in event:
                    events.append(e)

                track_indexes[i] += 1

                if track_indexes[i] == len(track):
                    track_indexes[i] = None
                    break

        for e in events:
            device.send_message(e)

        if done():
            break

        time.sleep(u)
        t += 1

    print('loop done')

one_bar = 4
def space(chords, t, v, start=0):
    a = []
    for i, c in enumerate(chords):
        a.append((on(c, v), start + i * one_bar))
        a.append((off(c), start + (i+t) * one_bar))

    return a
