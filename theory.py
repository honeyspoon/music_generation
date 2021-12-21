import itertools
import random
import math

plus = lambda x, y: x+y
def major_scale(note):
    steps = [2, 2, 1, 2, 2, 2, 1]

    return itertools.accumulate(steps, plus, initial=note)

def relative_note(note):
    # TODO
    return 4

step = 2 ** (1/12)
first_note_freq = 8.175799

def note_to_freq(note):
    return step ** note * first_note_freq

def freq_to_note(freq):
    note = math.log(freq / first_note_freq) / math.log(step)
    return round(note)

def overtones(note, n=None):
    last_note_freq = note_to_freq(127)
    freq = note_to_freq(note)

    smaller_than_last = lambda f: f <= last_note_freq
    if n:
        freqs = filter(smaller_than_last, (freq * i for i in range(1, n+1)))
    else:
        freqs = itertools.takewhile(smaller_than_last, (freq * i for i in itertools.count(1)))

    return list(map(freq_to_note, freqs))

def natural_minor_scale(note):
    steps = [2, 1, 2, 2, 1, 2, 2]
    return itertools.accumulate(steps, plus, initial=note)

def harmonic_minor_scale(base):
    natural = list(natural_minor_scale(base))
    natural[6] += 1

    return natural

def melodic_minor_scale(base):
    natural = list(natural_minor_scale(base))
    natural[5] += 1
    natural[6] += 1

    return natural


def random_chord(scale):
    chord = set()
    note = random.choice(scale)
    chord.add(note)

    while len(chord) != 3:
        note = random.choice(scale)
        note_index = scale.index(note)

        before_not_here = note_index -1 == 0 or scale[note_index -1 ] + 12 not in chord
        after_not_here = note_index + 1 != len(scale) -1 or scale[note_index + 1] + 12 not in chord

        if note not in chord and before_not_here and after_not_here:
            chord.add(note - 12)

    print(list(map(note_to_letter, chord)))

    return chord

letters = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def note_to_letter(note):
    l = len(letters)
    octave = note // l - 1
    letter = letters[note % l]

    return f"{letter}{octave}"
