import itertools
import collections
import random
import math

def minor_second(root):
    return root + 1
augmented_unison = minor_second

def major_second(root):
    return root + 2
diminished_third = major_second

def minor_third(root):
    return root + 3
augmented_second = minor_third

def major_third(root):
    return root + 4
diminished_fourth = major_third

def perfect_fourth(root):
    return root + 5
augmented_third = perfect_fourth

def diminished_fifth(root):
    return root + 6
augmented_fourth = diminished_fifth

def perfect_fifth(root):
    return root + 7
diminished_sixth = perfect_fifth

def minor_sixth(root):
    return root + 8
augmented_fifth = minor_sixth

def major_sixth(root):
    return root + 9
diminished_seventh = major_sixth

def minor_seventh(root):
    return root + 10
augmented_sixth = minor_seventh

def major_seventh(root):
    return root + 11
diminished_octave = major_seventh

def perfect_ocatave(root):
    return root + 12
augmented_seventh = perfect_ocatave

# chords
def diatonic_major_chord(root, degree):
    scale = major_scale(root)
    note = scale[degree]
    return [
        note + 0,
        note + 4,
        note + 7
    ]

def major_chord(root):
    return [root, major_third(root), perfect_fifth(root)]

def major_seventh_chord(root):
    return major_chord(root) + [major_seventh(root)]

def minor_chord(root):
    return [root, minor_third(root), perfect_fifth(root)]

def minor_seventh_chord(root):
    return minor_chord(root) + [minor_seventh(root)]

def augmented_triad(root):
    return [root, major_third(root), augmented_fifth(root)]

def diminished_triad(root):
    return [root, minor_third(root), diminished_fifth(root)]

def suspended_chord(root):
    return [root, perfect_fourth(root), perfect_fifth(root)]

chords = [
    major_chord,
    minor_chord,
    augmented_triad,
    diminished_triad,
    suspended_chord
]

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

def natural_minor_scale(root):
    return mode(root, 6)

def harmonic_minor_scale(base):
    natural = natural_minor_scale(base)
    natural[6] += 1

    return natural

def melodic_minor_scale(base):
    natural = natural_minor_scale(base)
    natural[5] += 1
    natural[6] += 1

    return natural

plus = lambda x, y: x+y
def mode(root, mode_num):
    steps = collections.deque([2, 2, 1, 2, 2, 2, 1])
    steps.rotate(mode_num - 1)

    return list(itertools.accumulate(steps, plus, initial=root))

def major_scale(root):
    return mode(root, 1)

def major_pentatonic_scale(root):
    steps = [7, 7, 7, 7]
    return list(itertools.accumulate(steps, plus, initial=root))

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

letters = ['C/B♭', 'C♯/D♭', 'D', 'D♯/E♭', 'E/F♭', 'F/E♯', 'F♯/G♭', 'G', 'G♯/A♭', 'A', 'A♯/B♭', 'B/C♭']

def note_to_letter(note):
    l = len(letters)
    octave = note // l - 1
    letter = letters[note % l]

    return f"{letter}{octave}"
